import os

#Fill exact DB Credentials
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bess_opt.db")
