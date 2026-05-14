use md5;
use hex;
use reqwest::Client;
use serde::Deserialize;
use std::time::{SystemTime, UNIX_EPOCH};

// --- Estruturas de Dados (Models) ---

#[derive(Deserialize, Debug)]
pub struct SubsonicResponse {
    #[serde(rename = "subsonic-response")]
    pub response: SubsonicData,
}

#[derive(Deserialize, Debug)]
pub struct SubsonicData {
    pub status: String,
    pub version: String,
    // O campo albumList2 só aparecerá em chamadas de álbuns
    #[serde(rename = "albumList2")]
    pub album_list: Option<AlbumList>,
}

#[derive(Deserialize, Debug)]
pub struct AlbumList {
    pub album: Vec<Album>,
}

#[derive(Deserialize, Debug)]
pub struct Album {
    pub id: String,
    pub title: String,
    pub artist: String,
    #[serde(rename = "coverArt")]
    pub cover_art: Option<String>,
}

// --- Cliente Principal ---

pub struct NavidromeClient {
    pub base_url: String,
    pub user: String,
    pass: String,
    client: Client,
}

impl NavidromeClient {
    /// Cria uma nova instância do cliente Navidrome
    pub fn new(base_url: &str, user: &str, pass: &str) -> Self {
        Self {
            base_url: base_url.trim_end_matches('/').to_string(),
            user: user.to_string(),
            pass: pass.to_string(),
            client: Client::new(),
        }
    }

    /// Gera os parâmetros de autenticação (Token + Salt) exigidos pelo protocolo Subsonic
    fn generate_auth_params(&self) -> String {
        let salt = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_millis()
            .to_string();

        let mut context = md5::Context::new();
        context.consume(self.pass.as_bytes());
        context.consume(salt.as_bytes());
        let token = format!("{:x}", context.compute());

        // c: nome do client, v: versão do protocolo, f: formato de resposta
        format!("u={}&t={}&s={}&v=1.16.1&c=Florune&f=json", self.user, token, salt)
    }

    /// Testa a conexão com o servidor
    pub async fn ping(&self) -> Result<String, Box<dyn std::error::Error>> {
        let auth = self.generate_auth_params();
        let url = format!("{}/rest/ping.view?{}", self.base_url, auth);

        let res: SubsonicResponse = self.client.get(&url).send().await?.json().await?;

        if res.response.status == "ok" {
            Ok(res.response.version)
        } else {
            Err("Falha na autenticação ou servidor indisponível".into())
        }
    }

    /// Busca uma lista de álbuns (ex: os mais recentes)
    pub async fn get_recent_albums(&self) -> Result<Vec<Album>, Box<dyn std::error::Error>> {
        let auth = self.generate_auth_params();
        // albumList2 com tipo 'newest'
        let url = format!("{}/rest/getAlbumList2.view?type=newest&size=20&{}", self.base_url, auth);

        let res: SubsonicResponse = self.client.get(&url).send().await?.json().await?;

        if let Some(list) = res.response.album_list {
            Ok(list.album)
        } else {
            Ok(vec![])
        }
    }
}
