from passlib.context import CryptContext
from subprocess import call
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Pdf thumbnail generator
# Make sure imagemagick is installed on machine
def generate_thumbnail(input_file, output_dir):
    output_file_name = os.path.basename(input_file).split('.')[0] + '.jpg'
    output = output_dir + output_file_name
    # cmd = ['convert', 
    #     input_file + '[0]',
    #     '-background', 'white', 
    #     '-alpha', 'background', 
    #     '-alpha', 
    #     'off',
    #     '-compress', 'JPEG',
    #     '-quality', '85%',
    #     '-gaussian-blur', '0.05', 
    #     output]
    # /home/derrick/app/src/backend/files/1b36a093-c02d-4ff0-9979-0f518b0cce9c.pdf[0] -background white -alpha background -alpha off -compress JPEG -quality 85% -gaussian-blur 0.05, /home/derrick/app/src/backend/files/thumbnails/test.png
    cmd = [f"convert {input_file}[0] -background white -alpha background -alpha off -compress JPEG -quality 85% -gaussian-blur 0.05, {output}"]
    call(cmd, shell=True)
    return output