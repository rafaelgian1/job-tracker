from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',env_file_encoding = 'utf-8')
    #case insensitive, match with env variables 
    postgres_user: str 
    postgres_password: str
    postgres_db: str
    postgres_host: str
#pydantic will automatically read the values from the .env file
#and populate the attributes of the Settings class based on the variable names 
#and their type of the attributes.