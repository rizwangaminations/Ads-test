//
//  DataEncryptor.cpp
//  cocos2d_libs
//
//  Created by RizwanAli on 04/04/2023.
//

#include "DataEncryptor.h"
#include <openssl/aes.h>
#include <openssl/evp.h>

NS_CC_BEGIN
using namespace std;

DataEncryptor::DataEncryptor(const string key, const string iv)
: m_key(key)
, m_iv(iv)
{
}

string DataEncryptor::decrypt(const string& encrypted_data)
{
    return decryptAES(encrypted_data);
}

string DataEncryptor::encrypt(const string& plaintext)
{
    return encryptAES(plaintext);
}

string DataEncryptor::encryptAES(const string& plaintext)
{
    string ciphertext;

    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_EncryptInit_ex(ctx, EVP_aes_128_cbc(), NULL,
                       reinterpret_cast<const unsigned char*>(m_key.c_str()),
                       reinterpret_cast<const unsigned char*>(m_iv.c_str()));

    int len = plaintext.length() + EVP_MAX_BLOCK_LENGTH;
    ciphertext.resize(len);
    int ciphertextLen;
    EVP_EncryptUpdate(ctx, reinterpret_cast<unsigned char*>(&ciphertext[0]),
                      &ciphertextLen,
                      reinterpret_cast<const unsigned char*>(plaintext.c_str()),
                      plaintext.length());
    int finalCiphertextLen;
    EVP_EncryptFinal_ex(ctx, reinterpret_cast<unsigned char*>(&ciphertext[0]) + ciphertextLen,
                        &finalCiphertextLen);
    ciphertext.resize(ciphertextLen + finalCiphertextLen);

    EVP_CIPHER_CTX_free(ctx);

    return ciphertext;
}

string DataEncryptor::decryptAES(const string& ciphertext)
{
    string plaintext;

    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_DecryptInit_ex(ctx, EVP_aes_128_cbc(), NULL,
                       reinterpret_cast<const unsigned char*>(m_key.c_str()),
                       reinterpret_cast<const unsigned char*>(m_iv.c_str()));

    int len = ciphertext.length() + EVP_MAX_BLOCK_LENGTH;
    plaintext.resize(len);
    int plaintextLen;
    EVP_DecryptUpdate(ctx, reinterpret_cast<unsigned char*>(&plaintext[0]),
                      &plaintextLen,
                      reinterpret_cast<const unsigned char*>(ciphertext.c_str()),
                      ciphertext.length());
    int finalPlaintextLen;
    EVP_DecryptFinal_ex(ctx, reinterpret_cast<unsigned char*>(&plaintext[0]) + plaintextLen,
                        &finalPlaintextLen);
    plaintext.resize(plaintextLen + finalPlaintextLen);

    EVP_CIPHER_CTX_free(ctx);

    return plaintext;
}

NS_CC_END
