# from pydantic import BaseSettings, SettingsConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

from cryptography.fernet import Fernet
import os


class Settings(BaseSettings):
    mongo_user_enc:str
    mongo_pass_enc:str
    mongo_host:str
    enc_key:str

    model_config = SettingsConfigDict(env_file=".env")

    # class Config:
    #     env_file=".env"
    
    @property
    def mongo_uri(self):
        f = Fernet(self.enc_key.encode())
        user=f.decrypt(self.mongo_user_enc.encode()).decode()
        password=f.decrypt(self.mongo_pass_enc.encode()).decode()
        return f"mongodb+srv://{user}:{password}@{self.mongo_host}/"
    

    
settings = Settings()


