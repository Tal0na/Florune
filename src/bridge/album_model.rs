use qmetaobject::*;
use crate::opensubsonic::models::Album;

#[derive(Clone, Default)]
pub struct AlbumItem {
    pub id: String,
    pub title: String,
    pub artist: String,
}

#[derive(QObject, Default)]
pub struct AlbumModel {
    base: qt_base_class!(trait QAbstractListModel),

    pub items: Vec<AlbumItem>,
}

impl AlbumModel {
    pub fn set_albums(
        &mut self,
        albums: Vec<Album>,
    ) {
        self.items = albums
            .into_iter()
            .map(|album| AlbumItem {
                id: album.id,
                title: album.name,
                artist: album.artist,
            })
            .collect();

        self.layout_changed();
    }
}

impl QAbstractListModel for AlbumModel {
    fn row_count(&self) -> i32 {
        self.items.len() as i32
    }

    fn data(
        &self,
        index: QModelIndex,
        role: i32,
    ) -> QVariant {
        let item = &self.items[index.row() as usize];

        match role {
            0 => QString::from(item.title.clone()).into(),
            1 => QString::from(item.artist.clone()).into(),
            2 => QString::from(item.id.clone()).into(),
            _ => QVariant::default(),
        }
    }

    fn role_names(
        &self,
    ) -> std::collections::HashMap<i32, QByteArray> {
        [
            (0, QByteArray::from("title")),
            (1, QByteArray::from("artist")),
            (2, QByteArray::from("albumId")),
        ]
        .into_iter()
        .collect()
    }
}
