use crate::opensubsonic::{client::NavidromeClient, models::Album};

pub fn fetch_albums(client: &NavidromeClient) -> Result<Vec<Album>, Box<dyn std::error::Error>> {
    let rt = tokio::runtime::Runtime::new()?;

    rt.block_on(async { client.get_recent_albums().await })
}
