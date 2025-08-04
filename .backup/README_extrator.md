# 🔵 Extrator de Conversa duEuler.com

Scripts Python para extrair mensagens de conversas com IA e gerar arquivos JSON estruturados.

## 📋 Descrição

Este projeto contém scripts para processar arquivos de conversa (como chats com ChatGPT) e extrair as mensagens da IA e do usuário, organizando-as em formato JSON estruturado para análise posterior.

## 🛠️ Scripts Disponíveis

### 1. `extract_chat.py` - Versão Básica
Script simples que extrai mensagens identificadas por:
- **IA**: "O ChatGPT disse:"
- **Usuário**: "Você disse:"

### 2. `extract_chat_advanced.py` - Versão Avançada
Script melhorado com:
- Múltiplos padrões de identificação
- Análise estatística da conversa
- Contagem de palavras
- Metadados detalhados

## 📊 Estrutura do JSON Gerado

```json
{
  "metadata": {
    "extracted_at": "2025-08-04T00:38:08.455217",
    "source_file": "backup/1 - nascimento.txt",
    "extractor_version": "2.0",
    "total_messages": 114
  },
  "conversation": [
    {
      "id": 1,
      "sender": "ia",
      "content": "Mensagem da IA...",
      "timestamp": null,
      "type": "text",
      "word_count": 407
    },
    {
      "id": 2,
      "sender": "usuario",
      "content": "Mensagem do usuário...",
      "timestamp": null,
      "type": "text",
      "word_count": 15
    }
  ],
  "analysis": {
    "total_messages": 114,
    "ia_messages": 57,
    "user_messages": 57,
    "total_words_ia": 14954,
    "total_words_user": 1850,
    "avg_words_ia": 262.35,
    "avg_words_user": 32.46,
    "conversation_ratio": "57:57",
    "first_sender": "ia",
    "last_sender": "usuario"
  }
}
```

## 🚀 Como Usar

### Execução Simples
```bash
# Versão básica
python extract_chat.py

# Versão avançada
python extract_chat_advanced.py
```

### Execução com Arquivo Específico
```bash
# Versão avançada com argumentos
python extract_chat_advanced.py "caminho/para/arquivo.txt"
```

## 📁 Arquivos Gerados

- `conversa_duEuler.json` - Versão básica
- `conversa_duEuler_avancada.json` - Versão com análise estatística

## 📈 Estatísticas Incluídas

### Análise da Conversa
- **Total de mensagens**: Número total de mensagens extraídas
- **Mensagens da IA**: Quantidade de mensagens da inteligência artificial
- **Mensagens do usuário**: Quantidade de mensagens do usuário
- **Proporção**: Relação entre mensagens da IA e do usuário
- **Contagem de palavras**: Total e média de palavras por tipo de mensagem
- **Primeira/Última mensagem**: Quem iniciou e terminou a conversa

### Metadados
- **Data/hora de extração**: Quando o processamento foi realizado
- **Arquivo de origem**: Caminho do arquivo processado
- **Versão do extrator**: Versão do script utilizado

## 🎯 Casos de Uso

### 1. Análise de Conversas
- Extrair insights de conversas com IA
- Analisar padrões de comunicação
- Estudar evolução de diálogos

### 2. Processamento de Dados
- Preparar dados para análise de sentimento
- Criar datasets para treinamento de IA
- Organizar histórico de conversas

### 3. Documentação
- Preservar conversas importantes
- Criar arquivos estruturados para referência
- Facilitar busca e análise posterior

## 🔧 Personalização

### Adicionar Novos Padrões
Para incluir outros formatos de conversa, edite os padrões regex no script:

```python
self.ia_patterns = [
    r'O ChatGPT disse:\s*\n(.*?)(?=\n\nVocê disse:|$)',
    r'Assistant:\s*\n(.*?)(?=\n\nUser:|$)',
    # Adicione seus padrões aqui
]
```

### Modificar Campos
Para adicionar novos campos às mensagens:

```python
all_messages.append({
    'id': message_id,
    'sender': 'ia',
    'content': msg.strip(),
    'timestamp': None,
    'type': 'text',
    'word_count': len(msg.split()),
    # Adicione seus campos aqui
    'custom_field': 'value'
})
```

## 📝 Exemplo de Saída

```
🔵 Extrator Avançado de Conversa duEuler.com
============================================================
📂 Processando: backup/1 - nascimento.txt

📊 RESUMO DA EXTRAÇÃO:
   📂 Arquivo: backup/1 - nascimento.txt
   📝 Total de mensagens: 114
   🤖 Mensagens da IA: 57
   👤 Mensagens do usuário: 57
   📊 Proporção: 57:57
   📈 Palavras IA: 14954 (média: 262.35)
   📈 Palavras Usuário: 1850 (média: 32.46)
   🎯 Primeira: ia
   🎯 Última: usuario
✅ JSON salvo: conversa_duEuler_avancada.json

🎉 Processamento concluído!
📄 JSON gerado: conversa_duEuler_avancada.json
```

## 🤝 Contribuição

Para contribuir com melhorias:

1. Clone o repositório
2. Faça suas modificações
3. Teste com diferentes formatos de arquivo
4. Envie um pull request

## 📄 Licença

Este projeto é parte do ecossistema duEuler.com e está disponível para uso pessoal e educacional.

---

**Desenvolvido com ❤️ para preservar e analisar conversas que tocam almas.** 