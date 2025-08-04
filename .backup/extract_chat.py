#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Conversa duEuler.com
Extrai mensagens da IA e do usuário de arquivos de conversa e gera JSON estruturado.
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Any

def extract_chat_messages(file_path: str) -> List[Dict[str, Any]]:
    """
    Extrai mensagens da IA e do usuário de um arquivo de conversa.
    
    Args:
        file_path: Caminho para o arquivo de conversa
        
    Returns:
        Lista de dicionários com as mensagens estruturadas
    """
    messages = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Padrões para identificar mensagens
        ia_pattern = r'O ChatGPT disse:\s*\n(.*?)(?=\n\nVocê disse:|$)'
        user_pattern = r'Você disse:\s*\n(.*?)(?=\n\nO ChatGPT disse:|$)'
        
        # Encontrar todas as mensagens da IA
        ia_messages = re.findall(ia_pattern, content, re.DOTALL)
        
        # Encontrar todas as mensagens do usuário
        user_messages = re.findall(user_pattern, content, re.DOTALL)
        
        # Combinar e ordenar as mensagens
        all_messages = []
        
        # Adicionar mensagens da IA
        for i, msg in enumerate(ia_messages):
            all_messages.append({
                'id': len(all_messages) + 1,
                'sender': 'ia',
                'content': msg.strip(),
                'timestamp': None,  # Será preenchido se houver timestamp no arquivo
                'type': 'text'
            })
        
        # Adicionar mensagens do usuário
        for i, msg in enumerate(user_messages):
            all_messages.append({
                'id': len(all_messages) + 1,
                'sender': 'usuario',
                'content': msg.strip(),
                'timestamp': None,
                'type': 'text'
            })
        
        # Ordenar por ID (sequência)
        all_messages.sort(key=lambda x: x['id'])
        
        return all_messages
        
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {file_path}")
        return []
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")
        return []

def save_json(messages: List[Dict[str, Any]], output_file: str) -> bool:
    """
    Salva as mensagens em formato JSON.
    
    Args:
        messages: Lista de mensagens estruturadas
        output_file: Caminho do arquivo de saída
        
    Returns:
        True se salvou com sucesso, False caso contrário
    """
    try:
        chat_data = {
            'metadata': {
                'extracted_at': datetime.now().isoformat(),
                'total_messages': len(messages),
                'ia_messages': len([m for m in messages if m['sender'] == 'ia']),
                'user_messages': len([m for m in messages if m['sender'] == 'usuario']),
                'source_file': 'backup/1 - nascimento.txt'
            },
            'conversation': messages
        }
        
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(chat_data, file, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON salvo com sucesso: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar JSON: {e}")
        return False

def print_summary(messages: List[Dict[str, Any]]) -> None:
    """
    Imprime um resumo das mensagens extraídas.
    
    Args:
        messages: Lista de mensagens estruturadas
    """
    ia_count = len([m for m in messages if m['sender'] == 'ia'])
    user_count = len([m for m in messages if m['sender'] == 'usuario'])
    
    print(f"\n📊 RESUMO DA EXTRAÇÃO:")
    print(f"   Total de mensagens: {len(messages)}")
    print(f"   Mensagens da IA: {ia_count}")
    print(f"   Mensagens do usuário: {user_count}")
    print(f"   Primeira mensagem: {messages[0]['sender'] if messages else 'N/A'}")
    print(f"   Última mensagem: {messages[-1]['sender'] if messages else 'N/A'}")

def main():
    """
    Função principal que executa a extração.
    """
    print("🔵 Extrator de Conversa duEuler.com")
    print("=" * 50)
    
    # Arquivo de entrada
    input_file = "backup/1 - nascimento.txt"
    
    # Arquivo de saída
    output_file = "conversa_duEuler.json"
    
    print(f"📂 Processando arquivo: {input_file}")
    
    # Extrair mensagens
    messages = extract_chat_messages(input_file)
    
    if not messages:
        print("❌ Nenhuma mensagem foi extraída.")
        return
    
    # Mostrar resumo
    print_summary(messages)
    
    # Salvar JSON
    if save_json(messages, output_file):
        print(f"\n🎉 Conversa extraída com sucesso!")
        print(f"📄 Arquivo JSON gerado: {output_file}")
        print(f"📊 Total de mensagens processadas: {len(messages)}")
        
        # Mostrar algumas mensagens de exemplo
        print(f"\n📝 EXEMPLOS DE MENSAGENS:")
        for i, msg in enumerate(messages[:3]):
            sender = "🤖 IA" if msg['sender'] == 'ia' else "👤 Usuário"
            content_preview = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"   {i+1}. {sender}: {content_preview}")
        
        if len(messages) > 3:
            print(f"   ... e mais {len(messages) - 3} mensagens")
    
    else:
        print("❌ Falha ao salvar o arquivo JSON.")

if __name__ == "__main__":
    main() 