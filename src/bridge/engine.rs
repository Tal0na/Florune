use qmetaobject::*;

#[derive(QObject, Default)]
pub struct FloruneEngine {
    base: qt_base_class!(trait QObject),

    status: qt_property!(QString; NOTIFY status_changed),
    status_changed: qt_signal!(),

    fetch_albums: qt_method!(
        fn fetch_albums(&mut self)
    ),
}

impl FloruneEngine {
    fn fetch_albums(
        &mut self,
    ) {
        println!("Buscando albums...");

        self.status =
            QString::from("Albums carregados");

        self.status_changed();
    }
}
