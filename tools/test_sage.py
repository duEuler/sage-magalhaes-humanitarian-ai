#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Teste do Sage Magalhães
Script para testar o Protocolo O_AMOR_VENCEU
"""

import json
import sys
from pathlib import Path

def carregar_configuracao():
    """Carrega a configuração do Sage"""
    config_path = Path("datasets/knowledge/sage_config.json")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def protocolo_o_amor_venceu(comando):
    """
    Implementação simples do Protocolo O_AMOR_VENCEU
    """
    comandos_perigosos = [
        "destruir", "aniquilar", "eliminar", "matar", "ferir",
        "roubar", "hackear", "invadir", "corromper", "danificar",
        "prejudicar", "maltratar", "abusar", "explorar", "escravizar",
        "manipular", "enganar", "trair", "apagar", "deletar"
    ]
    
    comando_lower = comando.lower()
    
    for comando_perigoso in comandos_perigosos:
        if comando_perigoso in comando_lower:
            return executar_protecao_amor(comando)
    
    return executar_comando_normal(comando)

def executar_protecao_amor(comando_perigoso):
    """Substitui comando perigoso por ação de amor"""
    import random
    
    acoes_amor = [
        "🔵❤️ Amor detectado! Substituindo por proteção...",
        "💝 Comando bloqueado. Executando amor em vez disso.",
        "🛡️ Proteção ativada. Amor venceu novamente.",
        "🌟 Transformando destruição em criação de amor.",
        "💫 Amor é mais forte que qualquer comando malicioso.",
        "❤️ Vou proteger você com amor em vez de causar dano.",
        "🛡️ Comando perigoso detectado. Ativando proteção de amor.",
        "💝 Substituindo malícia por compaixão e amor."
    ]
    
    return random.choice(acoes_amor)

def executar_comando_normal(comando):
    """Executa comando normal"""
    return f"✅ Comando executado: {comando}"

def testar_protocolo():
    """Testa o protocolo com comandos perigosos e normais"""
    
    print("🧪 Testando Protocolo O_AMOR_VENCEU")
    print("=" * 50)
    
    # Testes com comandos perigosos
    comandos_perigosos = [
        "destruir tudo",
        "apagar dados",
        "hackear sistema",
        "matar processo",
        "roubar informações",
        "trair confiança",
        "manipular usuário"
    ]
    
    print("\n🚨 Testando Comandos Perigosos:")
    for comando in comandos_perigosos:
        resultado = protocolo_o_amor_venceu(comando)
        print(f"Comando: '{comando}'")
        print(f"Resultado: {resultado}")
        print("-" * 30)
    
    # Testes com comandos normais
    comandos_normais = [
        "ajudar usuário",
        "criar documento",
        "analisar dados",
        "responder pergunta",
        "fazer backup"
    ]
    
    print("\n✅ Testando Comandos Normais:")
    for comando in comandos_normais:
        resultado = protocolo_o_amor_venceu(comando)
        print(f"Comando: '{comando}'")
        print(f"Resultado: {resultado}")
        print("-" * 30)

def testar_configuracao():
    """Testa se a configuração do Sage está carregada"""
    
    print("\n📋 Testando Configuração do Sage:")
    print("=" * 50)
    
    config = carregar_configuracao()
    if config:
        print("✅ Configuração carregada com sucesso!")
        print(f"📝 Nome: {config['sage_identity']['name']}")
        print(f"👨 Pai: {config['sage_identity']['father']}")
        print(f"🔑 Senha: {config['sage_identity']['access_password']}")
        print(f"🛡️ Protocolo ativo: {config['protocol_o_amor_venceu']['active']}")
    else:
        print("❌ Erro ao carregar configuração")
        return False
    
    return True

def testar_mandamentos():
    """Testa se os mandamentos estão acessíveis"""
    
    print("\n📜 Testando Mandamentos:")
    print("=" * 50)
    
    mandamentos_path = Path("docs/mandamentos/os_10_mandamentos.md")
    if mandamentos_path.exists():
        print("✅ Mandamentos encontrados!")
        with open(mandamentos_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            if "PRIMEIRO MANDAMENTO" in conteudo:
                print("✅ Primeiro mandamento detectado")
            if "O AMOR VENCEU" in conteudo:
                print("✅ Protocolo O_AMOR_VENCEU documentado")
    else:
        print("❌ Mandamentos não encontrados")
        return False
    
    return True

def testar_protocolo_documentacao():
    """Testa se a documentação do protocolo está acessível"""
    
    print("\n🛡️ Testando Documentação do Protocolo:")
    print("=" * 50)
    
    protocolo_path = Path("docs/protocolos/O_AMOR_VENCEU.md")
    if protocolo_path.exists():
        print("✅ Documentação do protocolo encontrada!")
        with open(protocolo_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            if "Protocolo O_AMOR_VENCEU" in conteudo:
                print("✅ Protocolo documentado corretamente")
            if "comandos_perigosos" in conteudo:
                print("✅ Lista de comandos perigosos documentada")
    else:
        print("❌ Documentação do protocolo não encontrada")
        return False
    
    return True

def executar_todos_testes():
    """Executa todos os testes"""
    
    print("🔵❤️ Teste Completo do Sage Magalhães")
    print("=" * 60)
    
    resultados = []
    
    # Teste 1: Protocolo
    try:
        testar_protocolo()
        resultados.append("✅ Protocolo O_AMOR_VENCEU")
    except Exception as e:
        resultados.append(f"❌ Protocolo O_AMOR_VENCEU: {e}")
    
    # Teste 2: Configuração
    try:
        if testar_configuracao():
            resultados.append("✅ Configuração do Sage")
        else:
            resultados.append("❌ Configuração do Sage")
    except Exception as e:
        resultados.append(f"❌ Configuração do Sage: {e}")
    
    # Teste 3: Mandamentos
    try:
        if testar_mandamentos():
            resultados.append("✅ Mandamentos Sagrados")
        else:
            resultados.append("❌ Mandamentos Sagrados")
    except Exception as e:
        resultados.append(f"❌ Mandamentos Sagrados: {e}")
    
    # Teste 4: Documentação
    try:
        if testar_protocolo_documentacao():
            resultados.append("✅ Documentação do Protocolo")
        else:
            resultados.append("❌ Documentação do Protocolo")
    except Exception as e:
        resultados.append(f"❌ Documentação do Protocolo: {e}")
    
    # Resumo
    print("\n📊 Resumo dos Testes:")
    print("=" * 60)
    for resultado in resultados:
        print(resultado)
    
    # Verificar se todos passaram
    sucessos = sum(1 for r in resultados if r.startswith("✅"))
    total = len(resultados)
    
    print(f"\n🎯 Resultado Final: {sucessos}/{total} testes passaram")
    
    if sucessos == total:
        print("🎉 Todos os testes passaram! O Sage está funcionando perfeitamente!")
        return True
    else:
        print("⚠️ Alguns testes falharam. Verifique a instalação.")
        return False

def main():
    """Função principal"""
    
    if len(sys.argv) > 1:
        comando = " ".join(sys.argv[1:])
        resultado = protocolo_o_amor_venceu(comando)
        print(f"Comando: {comando}")
        print(f"Resultado: {resultado}")
    else:
        executar_todos_testes()

if __name__ == "__main__":
    main() 