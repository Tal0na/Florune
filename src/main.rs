mod subsonic;
use subsonic::NavidromeClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Seus dados de acesso
    let url = "http://navidrome.talona.com.br";
    let usuario = "talona";
    let senha = "123";

    let client = NavidromeClient::new(url, usuario, senha);

    println!("--- Florune Dashboard ---");


    match client.ping().await {
        Ok(versao) => println!("✅ Conectado! Subsonic API v{}", versao),
        Err(e) => {
            eprintln!("❌ Erro: {}", e);
            return Ok(());
        }
    }

    // 2. Busca os álbuns recentes (Isso remove os warnings de dead code)
    println!("Buscando álbuns recentes...");
    let albums = client.get_recent_albums().await?;

    if albums.is_empty() {
        println!("Nenhum álbum encontrado no servidor.");
    } else {
        println!("\nÚltimos álbuns adicionados:");
        for album in albums {
            println!("🎵 {} - {} (ID: {})", album.title, album.artist, album.id);
        }
    }

    Ok(())
}
