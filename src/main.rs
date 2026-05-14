mod bridge;
mod opensubsonic;
mod services;
mod utils;

use bridge::engine::FloruneEngine;

use qmetaobject::*;

fn main() {
    qml_register_type::<FloruneEngine>(
        "Florune".into(),
        1,
        0,
        "FloruneEngine".into(),
    );

    let mut engine = QmlEngine::new();

    engine.load_file("ui/main.qml".into());

    engine.exec();
}
