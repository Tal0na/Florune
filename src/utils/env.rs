use dotenvy::dotenv;

pub fn load_env() {
    dotenv().ok();
}
