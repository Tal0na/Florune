use reqwest::Client;

pub struct NavidromeClient {
    pub client: Client,
    pub base_url: String,
    pub user: String,
    pub pass: String,
}

impl NavidromeClient {
    pub fn new(
        base_url: &str,
        user: &str,
        pass: &str,
    ) -> Self {
        Self {
            client: Client::new(),
            base_url: base_url.to_string(),
            user: user.to_string(),
            pass: pass.to_string(),
        }
    }

    pub fn from_env() -> Self {
        Self::new(
            &std::env::var("NAVIDROME_URL")
                .expect("NAVIDROME_URL missing"),
            &std::env::var("NAVIDROME_USER")
                .expect("NAVIDROME_USER missing"),
            &std::env::var("NAVIDROME_PASS")
                .expect("NAVIDROME_PASS missing"),
        )
    }
}
