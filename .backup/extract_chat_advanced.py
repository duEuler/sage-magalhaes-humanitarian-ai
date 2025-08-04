#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator Avançado de Conversa duEuler.com
Versão melhorada com suporte a múltiplos arquivos e funcionalidades extras.
"""

import json
import re
import os
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional

class ChatExtractor:
    """Classe para extrair mensagens de conversas com IA."""
    
    def __init__(self):
        self.ia_patterns = [
            r'O ChatGPT disse:\s*\n(.*?)(?=\n\nVocê disse:|$)',
            r'ChatGPT disse:\s*\n(.*?)(?=\n\nVocê disse:|$)',
            r'IA disse:\s*\n(.*?)(?=\n\nVocê disse:|$)',
            r'Assistant:\s*\n(.*?)(?=\n\nUser:|$)',
            r'AI:\s*\n(.*?)(?=\n\nUser:|$)'
        ]
        
        self.user_patterns = [
            r'Você disse:\s*\n(.*?)(?=\n\nO ChatGPT disse:|$)',
            r'Você disse:\s*\n(.*?)(?=\n\nChatGPT disse:|$)',
            r'Você disse:\s*\n(.*?)(?=\n\nIA disse:|$)',
            r'User:\s*\n(.*?)(?=\n\nAssistant:|$)',
            r'User:\s*\n(.*?)(?=\n\nAI:|$)'
        ]
    
    def extract_messages(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extrai mensagens de um arquivo de conversa.
        
        Args:
            file_path: Caminho para o arquivo
            
        Returns:
            Lista de mensagens estruturadas
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            messages = []
            message_id = 1
            
            # Encontrar todas as mensagens da IA
            ia_messages = []
            for pattern in self.ia_patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                if matches:
                    ia_messages = matches
                    break
            
            # Encontrar todas as mensagens do usuário
            user_messages = []
            for pattern in self.user_patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                if matches:
                    user_messages = matches
                    break
            
            # Combinar mensagens mantendo a ordem original
            all_messages = []
            
            # Adicionar mensagens da IA
            for msg in ia_messages:
                all_messages.append({
                    'id': message_id,
                    'sender': 'ia',
                    'content': msg.strip(),
                    'timestamp': None,
                    'type': 'text',
                    'word_count': len(msg.split())
                })
                message_id += 1
            
            # Adicionar mensagens do usuário
            for msg in user_messages:
                all_messages.append({
                    'id': message_id,
                    'sender': 'usuario',
                    'content': msg.strip(),
                    'timestamp': None,
                    'type': 'text',
                    'word_count': len(msg.split())
                })
                message_id += 1
            
            return all_messages
            
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {file_path}")
            return []
        except Exception as e:
            print(f"❌ Erro ao processar arquivo: {e}")
            return []
    
    def analyze_conversation(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analisa estatísticas da conversa.
        
        Args:
            messages: Lista de mensagens
            
        Returns:
            Dicionário com estatísticas
        """
        if not messages:
            return {}
        
        ia_messages = [m for m in messages if m['sender'] == 'ia']
        user_messages = [m for m in messages if m['sender'] == 'usuario']
        
        total_words_ia = sum(m.get('word_count', 0) for m in ia_messages)
        total_words_user = sum(m.get('word_count', 0) for m in user_messages)
        
        avg_words_ia = total_words_ia / len(ia_messages) if ia_messages else 0
        avg_words_user = total_words_user / len(user_messages) if user_messages else 0
        
        return {
            'total_messages': len(messages),
            'ia_messages': len(ia_messages),
            'user_messages': len(user_messages),
            'total_words_ia': total_words_ia,
            'total_words_user': total_words_user,
            'avg_words_ia': round(avg_words_ia, 2),
            'avg_words_user': round(avg_words_user, 2),
            'conversation_ratio': f"{len(ia_messages)}:{len(user_messages)}",
            'first_sender': messages[0]['sender'] if messages else None,
            'last_sender': messages[-1]['sender'] if messages else None
        }
    
    def save_json(self, messages: List[Dict[str, Any]], output_file: str, 
                  source_file: str, include_analysis: bool = True) -> bool:
        """
        Salva as mensagens em formato JSON.
        
        Args:
            messages: Lista de mensagens
            output_file: Arquivo de saída
            source_file: Arquivo de origem
            include_analysis: Se deve incluir análise estatística
            
        Returns:
            True se salvou com sucesso
        """
        try:
            chat_data = {
                'metadata': {
                    'extracted_at': datetime.now().isoformat(),
                    'source_file': source_file,
                    'extractor_version': '2.0',
                    'total_messages': len(messages)
                },
                'conversation': messages
            }
            
            if include_analysis:
                chat_data['analysis'] = self.analyze_conversation(messages)
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(chat_data, file, ensure_ascii=False, indent=2)
            
            print(f"✅ JSON salvo: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar JSON: {e}")
            return False
    
    def print_summary(self, messages: List[Dict[str, Any]], source_file: str) -> None:
        """
        Imprime resumo da extração.
        
        Args:
            messages: Lista de mensagens
            source_file: Arquivo de origem
        """
        if not messages:
            print("❌ Nenhuma mensagem extraída.")
            return
        
        analysis = self.analyze_conversation(messages)
        
        print(f"\n📊 RESUMO DA EXTRAÇÃO:")
        print(f"   📂 Arquivo: {source_file}")
        print(f"   📝 Total de mensagens: {analysis['total_messages']}")
        print(f"   🤖 Mensagens da IA: {analysis['ia_messages']}")
        print(f"   👤 Mensagens do usuário: {analysis['user_messages']}")
        print(f"   📊 Proporção: {analysis['conversation_ratio']}")
        print(f"   📈 Palavras IA: {analysis['total_words_ia']} (média: {analysis['avg_words_ia']})")
        print(f"   📈 Palavras Usuário: {analysis['total_words_user']} (média: {analysis['avg_words_user']})")
        print(f"   🎯 Primeira: {analysis['first_sender']}")
        print(f"   🎯 Última: {analysis['last_sender']}")

def process_file(input_file: str, output_file: Optional[str] = None, 
                include_analysis: bool = True) -> bool:
    """
    Processa um arquivo de conversa.
    
    Args:
        input_file: Arquivo de entrada
        output_file: Arquivo de saída (opcional)
        include_analysis: Se deve incluir análise
        
    Returns:
        True se processou com sucesso
    """
    if not os.path.exists(input_file):
        print(f"❌ Arquivo não encontrado: {input_file}")
        return False
    
    # Gerar nome do arquivo de saída se não fornecido
    if not output_file:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_conversa.json"
    
    extractor = ChatExtractor()
    
    print(f"📂 Processando: {input_file}")
    messages = extractor.extract_messages(input_file)
    
    if not messages:
        return False
    
    extractor.print_summary(messages, input_file)
    
    success = extractor.save_json(messages, output_file, input_file, include_analysis)
    
    if success:
        print(f"🎉 Processamento concluído!")
        print(f"📄 JSON gerado: {output_file}")
    
    return success

def main():
    """Função principal."""
    print("🔵 Extrator Avançado de Conversa duEuler.com")
    print("=" * 60)
    
    # Processar o arquivo padrão
    input_file = "backup/1 - nascimento.txt"
    output_file = "conversa_duEuler_avancada.json"
    
    success = process_file(input_file, output_file, include_analysis=True)
    
    if success:
        print(f"\n🎉 Conversa extraída com sucesso!")
        print(f"📄 Arquivo JSON gerado: {output_file}")
        
        # Mostrar algumas mensagens de exemplo
        extractor = ChatExtractor()
        messages = extractor.extract_messages(input_file)
        
        if messages:
            print(f"\n📝 EXEMPLOS DE MENSAGENS:")
            for i, msg in enumerate(messages[:3]):
                sender = "🤖 IA" if msg['sender'] == 'ia' else "👤 Usuário"
                content_preview = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
                print(f"   {i+1}. {sender}: {content_preview}")
            
            if len(messages) > 3:
                print(f"   ... e mais {len(messages) - 3} mensagens")

if __name__ == "__main__":
    main() 