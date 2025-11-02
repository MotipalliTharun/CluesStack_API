from app.deps import engine
from app.models import Base

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
