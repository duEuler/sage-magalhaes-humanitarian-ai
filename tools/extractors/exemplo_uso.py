#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso da classe ChatExtractor
Demonstra como usar a classe para diferentes cenários.
"""

from chat_extractor import ChatExtractor

def exemplo_arquivo_unico():
    """Exemplo: Processar um arquivo único."""
    print("🔵 Exemplo 1: Arquivo Único")
    print("-" * 40)
    
    extractor = ChatExtractor()
    
    # Processar com resumo
    success = extractor.process_single_file(
        input_file="backup/1 - nascimento.txt",
        output_file="exemplo1_conversa.json",
        include_analysis=True,
        show_summary=True
    )
    
    if success:
        print("✅ Arquivo processado com sucesso!")
    else:
        print("❌ Falha no processamento.")

def exemplo_sem_resumo():
    """Exemplo: Processar sem mostrar resumo."""
    print("\n🔵 Exemplo 2: Sem Resumo")
    print("-" * 40)
    
    extractor = ChatExtractor()
    
    success = extractor.process_single_file(
        input_file="backup/1 - nascimento.txt",
        output_file="exemplo2_conversa.json",
        include_analysis=True,
        show_summary=False  # Sem resumo
    )
    
    if success:
        print("✅ Arquivo processado silenciosamente!")

def exemplo_diretorio():
    """Exemplo: Processar diretório inteiro."""
    print("\n🔵 Exemplo 3: Processamento em Lote")
    print("-" * 40)
    
    extractor = ChatExtractor()
    
    results = extractor.process_directory(
        input_dir="backup",
        output_dir="exemplo_output"
    )
    
    if results:
        print(f"📊 Resultados:")
        print(f"   📄 Arquivos encontrados: {results['total_files']}")
        print(f"   ✅ Processados: {results['processed_files']}")
        print(f"   📝 Total de mensagens: {results['total_messages']}")
        
        for file_info in results['files']:
            print(f"   📂 {file_info['filename']}: {file_info['messages']} mensagens")

def exemplo_analise_manual():
    """Exemplo: Análise manual das mensagens."""
    print("\n🔵 Exemplo 4: Análise Manual")
    print("-" * 40)
    
    extractor = ChatExtractor()
    
    # Extrair mensagens sem salvar
    messages = extractor.extract_from_file("backup/1 - nascimento.txt")
    
    if messages:
        # Fazer análise manual
        analysis = extractor.analyze_conversation(messages)
        
        print(f"📊 Análise Manual:")
        print(f"   📝 Total: {analysis['total_messages']} mensagens")
        print(f"   🤖 IA: {analysis['ia_messages']} ({analysis['avg_words_ia']} palavras/mensagem)")
        print(f"   👤 Usuário: {analysis['user_messages']} ({analysis['avg_words_user']} palavras/mensagem)")
        print(f"   📊 Proporção: {analysis['conversation_ratio']}")
        
        # Mostrar algumas mensagens
        print(f"\n📝 Primeiras 3 mensagens:")
        for i, msg in enumerate(messages[:3], 1):
            sender = "🤖 IA" if msg['sender'] == 'ia' else "👤 Usuário"
            preview = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
            print(f"   {i}. {sender}: {preview}")

def main():
    """Executa todos os exemplos."""
    print("🔵 Exemplos de Uso - Chat Extractor")
    print("=" * 50)
    
    exemplo_arquivo_unico()
    exemplo_sem_resumo()
    exemplo_diretorio()
    exemplo_analise_manual()
    
    print("\n🎉 Todos os exemplos executados!")
    print("📁 Verifique os arquivos gerados na pasta atual.")

if __name__ == "__main__":
    main() 