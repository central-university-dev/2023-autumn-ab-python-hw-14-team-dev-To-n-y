from fastapi import FastAPI

from .routers import auth, posts, subscriptions

app = FastAPI(
    title="Tinkoff HW Blog API",
    version="0.0.1",
    docs_url="/docs",
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(subscriptions.router)
