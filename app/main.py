from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.db.base import Base
from app.db.session import engine
from app.api.router import router
from app.core.config import settings
from app.core.security import SecurityHeadersMiddleware
from app.models import User, PublishJob  # مهم جداً لاستيراد الموديل

# إعداد محدد معدل الطلبات
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])

# إخفاء التوثيق التفاعلي في بيئة الإنتاج
docs_url = "/docs" if settings.ENVIRONMENT != "production" else None
redoc_url = "/redoc" if settings.ENVIRONMENT != "production" else None

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Rooz Social Publishing Server",
    version=settings.APP_VERSION,
    docs_url=docs_url,
    redoc_url=redoc_url,
)

# تسجيل محدد معدل الطلبات
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# وسيط الرؤوس الأمنية
app.add_middleware(SecurityHeadersMiddleware)

# وسيط CORS - حماية من الطلبات عبر النطاقات
cors_origins = (
    [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
    if settings.CORS_ORIGINS
    else []
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# وسيط المضيفين الموثوقين - حماية من هجمات Host Header
allowed_hosts = (
    [h.strip() for h in settings.ALLOWED_HOSTS.split(",") if h.strip()]
    if settings.ALLOWED_HOSTS
    else ["*"]
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# إنشاء الجداول عند بدء التشغيل
Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/health", tags=["health"])
@limiter.limit("120/minute")
async def health_check(request: Request):
    return {"status": "ok", "service": settings.APP_NAME}
