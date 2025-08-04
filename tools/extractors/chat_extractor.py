#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chat Extractor - Classe única para extração de conversas com IA
Versão refatorada e otimizada do sistema de extração duEuler.com
"""

import json
import re
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class ChatExtractor:
    """
    Classe principal para extração e análise de conversas com IA.
    Combina todas as funcionalidades em uma única classe eficiente.
    """
    
    def __init__(self):
        """Inicializa o extrator com padrões de identificação."""
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
    
    def extract_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extrai mensagens de um arquivo de conversa mantendo a ordem cronológica.
        
        Args:
            file_path: Caminho para o arquivo
            
        Returns:
            Lista de mensagens estruturadas em ordem cronológica
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            messages = []
            message_id = 1
            
            # Dividir o conteúdo em seções baseadas nos marcadores
            sections = []
            
            # Padrão para encontrar todas as seções
            pattern = r'(?:O ChatGPT disse:\s*\n|Você disse:\s*\n)(.*?)(?=\n\n(?:O ChatGPT disse:|Você disse:)|$)'
            matches = re.findall(pattern, content, re.DOTALL)
            
            # Encontrar os marcadores para determinar a ordem
            markers = re.findall(r'(O ChatGPT disse:|Você disse:)', content)
            
            # Verificar se há uma primeira mensagem do usuário (antes de "O ChatGPT disse:")
            first_part = content.split('O ChatGPT disse:')[0].strip()
            if first_part and not first_part.startswith('Você disse:'):
                # Adicionar primeira mensagem do usuário
                messages.append({
                    'id': message_id,
                    'sender': 'usuario',
                    'content': first_part,
                    'timestamp': None,
                    'type': 'text',
                    'word_count': len(first_part.split())
                })
                message_id += 1
            
            # Processar as mensagens em ordem cronológica
            current_pos = 0
            for i, marker in enumerate(markers):
                if marker == 'O ChatGPT disse:':
                    # Encontrar o conteúdo da IA
                    start = content.find('O ChatGPT disse:', current_pos)
                    end = content.find('Você disse:', start)
                    if end == -1:
                        end = len(content)
                    
                    ia_content = content[start + len('O ChatGPT disse:'):end].strip()
                    if ia_content:
                        messages.append({
                            'id': message_id,
                            'sender': 'ia',
                            'content': ia_content,
                            'timestamp': None,
                            'type': 'text',
                            'word_count': len(ia_content.split())
                        })
                        message_id += 1
                    
                    current_pos = end
                
                elif marker == 'Você disse:':
                    # Encontrar o conteúdo do usuário
                    start = content.find('Você disse:', current_pos)
                    end = content.find('O ChatGPT disse:', start)
                    if end == -1:
                        end = len(content)
                    
                    user_content = content[start + len('Você disse:'):end].strip()
                    if user_content:
                        messages.append({
                            'id': message_id,
                            'sender': 'usuario',
                            'content': user_content,
                            'timestamp': None,
                            'type': 'text',
                            'word_count': len(user_content.split())
                        })
                        message_id += 1
                    
                    current_pos = end
            
            return messages
            
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
                    'extractor_version': '3.0',
                    'total_messages': len(messages)
                },
                'conversation': messages
            }
            
            if include_analysis:
                chat_data['analysis'] = self.analyze_conversation(messages)
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(chat_data, file, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar JSON: {e}")
            return False
    
    def process_single_file(self, input_file: str, output_file: Optional[str] = None, 
                           include_analysis: bool = True, show_summary: bool = True) -> bool:
        """
        Processa um arquivo único de conversa.
        
        Args:
            input_file: Arquivo de entrada
            output_file: Arquivo de saída (opcional)
            include_analysis: Se deve incluir análise
            show_summary: Se deve mostrar resumo
            
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
        
        print(f"📂 Processando: {input_file}")
        
        # Extrair mensagens
        messages = self.extract_from_file(input_file)
        
        if not messages:
            return False
        
        # Mostrar resumo se solicitado
        if show_summary:
            self.print_summary(messages, input_file)
        
        # Salvar JSON
        success = self.save_json(messages, output_file, input_file, include_analysis)
        
        if success:
            print(f"✅ JSON salvo: {output_file}")
            return True
        
        print(f"❌ Falha ao salvar: {output_file}")
        return False
    
    def process_directory(self, input_dir: str, output_dir: str = "extracted_conversations") -> Dict[str, Any]:
        """
        Processa todos os arquivos .txt em um diretório.
        
        Args:
            input_dir: Diretório de entrada
            output_dir: Diretório de saída
            
        Returns:
            Dicionário com estatísticas do processamento
        """
        # Criar diretório de saída se não existir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"📁 Diretório criado: {output_dir}")
        
        # Encontrar arquivos .txt
        txt_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
        
        if not txt_files:
            print(f"❌ Nenhum arquivo .txt encontrado em: {input_dir}")
            return {}
        
        print(f"🔵 Processando {len(txt_files)} arquivos...")
        
        results = {
            'total_files': len(txt_files),
            'processed_files': 0,
            'total_messages': 0,
            'files': []
        }
        
        # Processar cada arquivo
        for txt_file in txt_files:
            input_path = os.path.join(input_dir, txt_file)
            base_name = os.path.splitext(txt_file)[0]
            output_file = os.path.join(output_dir, f"{base_name}_conversa.json")
            
            messages = self.extract_from_file(input_path)
            
            if messages:
                success = self.save_json(messages, output_file, input_path, include_analysis=True)
                
                if success:
                    results['processed_files'] += 1
                    results['total_messages'] += len(messages)
                    
                    analysis = self.analyze_conversation(messages)
                    results['files'].append({
                        'filename': txt_file,
                        'output_file': f"{base_name}_conversa.json",
                        'messages': len(messages),
                        'analysis': analysis
                    })
        
        return results
    
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
        
        print(f"\n📊 RESUMO:")
        print(f"   📂 Arquivo: {source_file}")
        print(f"   📝 Mensagens: {analysis['total_messages']}")
        print(f"   🤖 IA: {analysis['ia_messages']}")
        print(f"   👤 Usuário: {analysis['user_messages']}")
        print(f"   📊 Proporção: {analysis['conversation_ratio']}")
        print(f"   📈 Palavras: {analysis['total_words_ia'] + analysis['total_words_user']}")

def main():
    """Função principal para uso direto do script."""
    print("🔵 Chat Extractor - duEuler.com")
    print("=" * 50)
    
    extractor = ChatExtractor()
    
    # Processar arquivo padrão
    input_file = "datasets/conversations/backup/1 - nascimento.txt"
    output_file = "conversa_duEuler.json"
    
    if extractor.process_single_file(input_file, output_file):
        print(f"\n🎉 Conversa extraída com sucesso!")
        print(f"📄 Arquivo: {output_file}")
    else:
        print("❌ Falha no processamento.")

if __name__ == "__main__":
    main() 