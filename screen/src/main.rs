use std::{thread, time};
use std::borrow::Borrow;
use std::convert::Infallible;
use std::net::SocketAddr;

use log::{self, info, error};
use simple_logger::SimpleLogger;

use push2_display::Push2Display;
use embedded_graphics::{
    mono_font::{ascii::Font10x20, MonoTextStyle},
    pixelcolor::Bgr565,
    prelude::*,
    text::Text,
};

use tokio;
use hyper::service::{service_fn, make_service_fn};
use hyper::{Request, Body, Response, Server};

static mut DATA: String = String::new();

fn main() {
    SimpleLogger::new().init().unwrap();

    info!("Opening display connection");
    let mut display = Push2Display::new().unwrap();

    info!("clearing display");
    display.clear(Bgr565::BLACK).unwrap();

    info!("Starting hyper webserver");
    thread::spawn(|| {
        return server();
    });

    unsafe {
        DATA.push_str("I <3 Rust");
        loop {
            display.clear(Bgr565::BLACK).unwrap();
            Text::new(DATA.borrow(), Point::new(10, 20))
                .into_styled(MonoTextStyle::new(Font10x20, Bgr565::GREEN))
                .draw(&mut display).unwrap();
            display.flush().unwrap(); // if no frame arrives in 2 seconds, the display is turned black
            thread::sleep(time::Duration::from_millis(1000 / 60));
        }
    }
}

#[tokio::main]
async fn server() {
    // We'll bind to 127.0.0.1:3000
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));

    // A `Service` is needed for every connection, so this
    // creates one from our `hello_world` function.
    let make_svc = make_service_fn(|_conn| async {
        // service_fn converts our function into a `Service`
        Ok::<_, Infallible>(service_fn(hello_world))
    });

    let server = Server::bind(&addr).serve(make_svc);

    // Run this server for... forever!
    if let Err(e) = server.await {
        error!("server error: {}", e);
    }
}

async fn hello_world(_req: Request<Body>) -> Result<Response<Body>, Infallible> {
    let bytes = hyper::body::to_bytes(_req.into_body()).await.unwrap();
    let result = String::from_utf8(bytes.into_iter().collect()).expect("");
    let test = result.to_owned();
    unsafe {
        DATA = test;
        info!("New request with body: \"{}\"", DATA);
    }
    Ok(Response::new(result.into()))
}
