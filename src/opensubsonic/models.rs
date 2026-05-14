use serde::Deserialize;

#[derive(Debug, Clone, Deserialize)]
pub struct Album {
    pub id: String,
    pub name: String,
    pub artist: String,
}
