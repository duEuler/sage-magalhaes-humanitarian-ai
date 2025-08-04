#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador em Lote de Conversas duEuler.com
Processa múltiplos arquivos de conversa de uma vez.
"""

import os
import json
from datetime import datetime
from extract_chat_advanced import ChatExtractor

def process_directory(directory_path: str, output_dir: str = "extracted_conversations") -> None:
    """
    Processa todos os arquivos .txt em um diretório.
    
    Args:
        directory_path: Caminho do diretório com arquivos
        output_dir: Diretório de saída para os JSONs
    """
    # Criar diretório de saída se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Diretório criado: {output_dir}")
    
    # Encontrar todos os arquivos .txt
    txt_files = []
    for file in os.listdir(directory_path):
        if file.endswith('.txt'):
            txt_files.append(file)
    
    if not txt_files:
        print(f"❌ Nenhum arquivo .txt encontrado em: {directory_path}")
        return
    
    print(f"🔵 Processador em Lote de Conversas duEuler.com")
    print("=" * 60)
    print(f"📁 Diretório: {directory_path}")
    print(f"📄 Arquivos encontrados: {len(txt_files)}")
    print(f"📂 Saída: {output_dir}")
    print()
    
    extractor = ChatExtractor()
    success_count = 0
    total_messages = 0
    
    # Processar cada arquivo
    for i, txt_file in enumerate(txt_files, 1):
        input_path = os.path.join(directory_path, txt_file)
        base_name = os.path.splitext(txt_file)[0]
        output_file = os.path.join(output_dir, f"{base_name}_conversa.json")
        
        print(f"📂 [{i}/{len(txt_files)}] Processando: {txt_file}")
        
        # Extrair mensagens
        messages = extractor.extract_messages(input_path)
        
        if messages:
            # Salvar JSON
            success = extractor.save_json(messages, output_file, input_path, include_analysis=True)
            
            if success:
                success_count += 1
                total_messages += len(messages)
                
                # Mostrar resumo rápido
                analysis = extractor.analyze_conversation(messages)
                print(f"   ✅ Extraídas: {analysis['total_messages']} mensagens")
                print(f"   📊 Proporção: {analysis['conversation_ratio']}")
                print(f"   📈 Palavras: {analysis['total_words_ia'] + analysis['total_words_user']}")
            else:
                print(f"   ❌ Erro ao salvar: {output_file}")
        else:
            print(f"   ⚠️ Nenhuma mensagem extraída")
        
        print()
    
    # Relatório final
    print("🎉 PROCESSAMENTO CONCLUÍDO!")
    print("=" * 60)
    print(f"📄 Arquivos processados: {success_count}/{len(txt_files)}")
    print(f"📝 Total de mensagens: {total_messages}")
    print(f"📂 Arquivos JSON gerados em: {output_dir}")
    
    if success_count > 0:
        print(f"\n📋 Arquivos gerados:")
        for file in os.listdir(output_dir):
            if file.endswith('_conversa.json'):
                file_path = os.path.join(output_dir, file)
                file_size = os.path.getsize(file_path) / 1024  # KB
                print(f"   📄 {file} ({file_size:.1f} KB)")

def create_summary_report(output_dir: str) -> None:
    """
    Cria um relatório resumido de todas as conversas processadas.
    
    Args:
        output_dir: Diretório com os JSONs gerados
    """
    json_files = [f for f in os.listdir(output_dir) if f.endswith('_conversa.json')]
    
    if not json_files:
        print("❌ Nenhum arquivo JSON encontrado para relatório")
        return
    
    summary = {
        'report_generated_at': datetime.now().isoformat(),
        'total_files_processed': len(json_files),
        'total_messages_across_all': 0,
        'total_ia_messages': 0,
        'total_user_messages': 0,
        'total_words_ia': 0,
        'total_words_user': 0,
        'files': []
    }
    
    print(f"\n📊 GERANDO RELATÓRIO RESUMIDO...")
    
    for json_file in json_files:
        file_path = os.path.join(output_dir, json_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            analysis = data.get('analysis', {})
            
            file_summary = {
                'filename': json_file,
                'source_file': data.get('metadata', {}).get('source_file', ''),
                'total_messages': analysis.get('total_messages', 0),
                'ia_messages': analysis.get('ia_messages', 0),
                'user_messages': analysis.get('user_messages', 0),
                'total_words_ia': analysis.get('total_words_ia', 0),
                'total_words_user': analysis.get('total_words_user', 0),
                'avg_words_ia': analysis.get('avg_words_ia', 0),
                'avg_words_user': analysis.get('avg_words_user', 0)
            }
            
            summary['files'].append(file_summary)
            summary['total_messages_across_all'] += file_summary['total_messages']
            summary['total_ia_messages'] += file_summary['ia_messages']
            summary['total_user_messages'] += file_summary['user_messages']
            summary['total_words_ia'] += file_summary['total_words_ia']
            summary['total_words_user'] += file_summary['total_words_user']
            
        except Exception as e:
            print(f"❌ Erro ao processar {json_file}: {e}")
    
    # Calcular médias
    if summary['total_ia_messages'] > 0:
        summary['avg_words_ia_overall'] = summary['total_words_ia'] / summary['total_ia_messages']
    if summary['total_user_messages'] > 0:
        summary['avg_words_user_overall'] = summary['total_words_user'] / summary['total_user_messages']
    
    # Salvar relatório
    report_file = os.path.join(output_dir, "relatorio_geral.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Relatório salvo: {report_file}")
    
    # Mostrar resumo
    print(f"\n📈 RESUMO GERAL:")
    print(f"   📄 Arquivos processados: {summary['total_files_processed']}")
    print(f"   📝 Total de mensagens: {summary['total_messages_across_all']}")
    print(f"   🤖 Mensagens da IA: {summary['total_ia_messages']}")
    print(f"   👤 Mensagens do usuário: {summary['total_user_messages']}")
    print(f"   📊 Proporção geral: {summary['total_ia_messages']}:{summary['total_user_messages']}")
    print(f"   📈 Total de palavras: {summary['total_words_ia'] + summary['total_words_user']}")

def main():
    """Função principal."""
    # Diretório padrão
    input_dir = "backup"
    output_dir = "extracted_conversations"
    
    if not os.path.exists(input_dir):
        print(f"❌ Diretório não encontrado: {input_dir}")
        print("💡 Certifique-se de que o diretório 'backup' existe com arquivos .txt")
        return
    
    # Processar arquivos
    process_directory(input_dir, output_dir)
    
    # Gerar relatório
    create_summary_report(output_dir)
    
    print(f"\n🎉 Tudo pronto! Verifique a pasta '{output_dir}' para os resultados.")

if __name__ == "__main__":
    main() 