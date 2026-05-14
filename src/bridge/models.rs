use qmetaobject::*;

#[derive(Clone, Default)]
pub struct AlbumItem {
    pub title: QString,
    pub artist: QString,
    pub album_id: QString,
}

impl SimpleListItem for AlbumItem {
    fn get(&self, role: i32) -> QVariant {
        match role {
            0 => self.title.clone().into(),
            1 => self.artist.clone().into(),
            2 => self.album_id.clone().into(),
            _ => QVariant::default(),
        }
    }

    fn names() -> Vec<QByteArray> {
        vec![
            QByteArray::from("title"),
            QByteArray::from("artist"),
            QByteArray::from("albumId"),
        ]
    }
}
