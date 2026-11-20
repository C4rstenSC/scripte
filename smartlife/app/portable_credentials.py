"""Cross-platform encrypted credential bundle. No decryption key in source or GitHub."""
import base64,json,os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
MAGIC=b'SMARTLIFE-CREDENTIALS-1\n'

def encrypt_config(config,password):
    if len(password)<12:raise ValueError('Bitte ein Entschlüsselungskennwort mit mindestens 12 Zeichen verwenden.')
    salt=os.urandom(16);nonce=os.urandom(12)
    key=Scrypt(salt=salt,length=32,n=32768,r=8,p=1).derive(password.encode('utf-8'))
    raw=json.dumps(config,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    cipher=AESGCM(key).encrypt(nonce,raw,MAGIC)
    return MAGIC+base64.b64encode(salt+nonce+cipher)+b'\n'

def decrypt_config(blob,password):
    if len(blob)>65536 or not blob.startswith(MAGIC):raise ValueError('Dies ist keine unterstützte verschlüsselte Smart-Life-Datei.')
    try:
        raw=base64.b64decode(blob[len(MAGIC):].strip(),validate=True)
        if len(raw)<45:raise ValueError()
        key=Scrypt(salt=raw[:16],length=32,n=32768,r=8,p=1).derive(password.encode('utf-8'))
        result=json.loads(AESGCM(key).decrypt(raw[16:28],raw[28:],MAGIC))
        if not isinstance(result,dict) or not all(isinstance(result.get(k),str) for k in ('access_id','access_secret','uid','region')):raise ValueError()
        return result
    except Exception as e:raise ValueError('Datei konnte nicht entschlüsselt werden. Kennwort oder Dateiintegrität prüfen.') from e
