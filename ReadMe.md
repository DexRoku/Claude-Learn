# Claude with the Anthropic API - Course Repository

## 📚 About This Repository

This repository contains my work and projects from Anthropic's **"Claude with the Anthropic API"** course. This comprehensive course covers everything from basic API usage to advanced topics like RAG, tool use, and building AI agents with Claude.

## 🎯 Course Overview

The course is structured into several key modules covering:

- **API Fundamentals**: Getting started with Claude's API, authentication, and basic requests
- **Prompt Engineering**: Techniques for effective prompting and output control
- **Tool Use**: Integrating Claude with external tools and APIs
- **Retrieval Augmented Generation (RAG)**: Building knowledge-enhanced applications
- **Advanced Features**: Image support, PDF processing, prompt caching, and more
- **Model Context Protocol (MCP)**: Creating custom integrations
- **Agents & Workflows**: Building sophisticated AI workflows
- **Anthropic Apps**: Claude Code and computer use capabilities

## 🛠️ Technologies Used

- **API**: Anthropic Claude API
- **Languages**: Python, JavaScript (depending on exercises)
- **Libraries**: 
  - `anthropic` (Python/JS SDK)
  - Various tool integration libraries
  - Embedding and vector databases for RAG
- **Tools**: 
  - Claude Code
  - MCP servers and clients
  - Text processing and chunking tools

## 📁 Repository Structure

```
drwxr-xr-x@ 10 dexter  staff   320 Aug 29 14:55 .
drwxr-xr-x@  4 dexter  staff   128 Aug 20 16:06 ..
drwxr-xr-x@ 13 dexter  staff   416 Aug 29 15:13 .git
-rw-r--r--@  1 dexter  staff   402 Aug 20 16:06 .gitignore
drwxr-xr-x@  7 dexter  staff   224 Aug 29 14:55 01-api-basics
drwxr-xr-x@ 12 dexter  staff   384 Aug 24 15:55 02-prompt-engineering
drwxr-xr-x   3 dexter  staff    96 Aug 29 14:56 03-tool-use-claude
-rw-r--r--@  1 dexter  staff  5658 Aug 20 16:09 ReadMe.md
drwxr-xr-x   3 dexter  staff    96 Aug 23 21:59 __pycache__
-rw-r--r--@  1 dexter  staff  2034 Aug 20 16:06 interactive_chat.py

```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ or Node.js 16+
- Anthropic API key
- Basic understanding of REST APIs

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/claude-api-course.git
   cd claude-api-course
   ```

2. Install dependencies:
   ```bash
   # For Python
   pip install anthropic python-dotenv requests
   
   # For JavaScript
   npm install @anthropic-ai/sdk dotenv
   ```

3. Set up your API key:
   ```bash
   # Create .env file
   echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
   ```

### Running Examples

Each module contains its own README with specific instructions. Generally:

```bash
cd [module-folder]
python main.py  # or node main.js
```

## 📋 Key Learning Modules

### 🔑 API Basics
- Authentication and API key management
- Making your first API requests
- Handling multi-turn conversations
- System prompts and temperature control

### 🎨 Prompt Engineering
- Clear and direct communication
- Structuring prompts with XML tags
- Providing effective examples
- Controlling model output

### 🔧 Tool Use
- Defining and using tool functions
- Multi-turn tool conversations
- Batch processing with tools
- Web search and data tools

### 📚 Retrieval Augmented Generation (RAG)
- Text chunking strategies
- Embedding generation and similarity search
- Full RAG pipeline implementation
- Multi-index and reranking approaches

### ⚡ Advanced Features
- Extended thinking capabilities
- Multimodal support (images, PDFs)
- Citation and source tracking
- Prompt caching for efficiency

### 🤖 Agents & Workflows
- Building parallel processing workflows
- Chaining operations together
- Routing and decision-making
- Environment inspection and adaptation

## 🎓 Learning Outcomes

Through this course, I've gained hands-on experience with:

- **API Integration**: Seamlessly integrating Claude into applications
- **Prompt Optimization**: Crafting effective prompts for various use cases
- **Tool Development**: Building custom tools and integrations
- **RAG Systems**: Creating knowledge-enhanced AI applications
- **Agent Architecture**: Designing sophisticated AI workflows
- **Performance Optimization**: Using caching and efficient patterns
- **Evaluation Methods**: Testing and improving AI system performance

## 🔬 Projects & Exercises

### Chat Applications
Built various chat interfaces demonstrating multi-turn conversations and context management.

### Tool Integration Projects
Created custom tools for web search, data processing, and API integrations.

### RAG Implementation
Developed a complete retrieval-augmented generation system with multiple indexing strategies.

### AI Agent Workflows
Built agents capable of complex multi-step reasoning and task execution.

## 📚 Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com)
- [Claude Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Course Materials](https://anthropic.skilljar.com/claude-with-the-anthropic-api)

## 📝 Notes

- All code examples follow best practices for API usage and error handling
- Each module includes both basic and advanced implementations
- Environment variables are used for secure API key management
- Code is documented and includes example outputs

## 🤝 Contributing

While this is a personal learning repository, I welcome:
- Bug reports and fixes
- Code improvements and optimizations
- Additional examples and use cases
- Documentation enhancements

## 📄 License

This project is for educational purposes as part of Anthropic's official course. Code examples and implementations are available under MIT license for learning and adaptation.

---

**Course**: Claude with the Anthropic API  
**Provider**: Anthropic  
**Platform**: Skilljar  
**Completed**: [Your completion date]

## 🏆 Course Completion

- ✅ All modules completed
- ✅ All exercises and quizzes passed  
- ✅ Final assessment completed
- ✅ Certificate earned

*This repository represents my journey learning to build with Claude and the Anthropic API, from basic interactions to sophisticated AI agents and workflows.*