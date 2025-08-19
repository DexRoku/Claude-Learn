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
├── 01-api-basics/              # API access and basic requests
│   ├── getting-started/        # First API calls
│   ├── multi-turn-chat/        # Conversation handling
│   └── system-prompts/         # System prompt exercises
├── 02-prompt-engineering/      # Prompt engineering techniques
│   ├── clear-direct/           # Being clear and direct
│   ├── xml-structure/          # Using XML tags
│   └── examples/               # Providing examples
├── 03-prompt-evaluation/       # Evaluation and testing
│   ├── test-datasets/          # Generating test data
│   ├── model-grading/          # Model-based evaluation
│   └── code-grading/           # Code-based evaluation
├── 04-tool-use/               # Tool integration
│   ├── basic-tools/            # Simple tool functions
│   ├── multi-turn-tools/       # Complex tool workflows
│   ├── batch-processing/       # Batch tool operations
│   └── web-search-tools/       # Web search integration
├── 05-rag/                    # Retrieval Augmented Generation
│   ├── text-chunking/          # Chunking strategies
│   ├── embeddings/             # Text embeddings
│   ├── full-rag-flow/          # Complete RAG pipeline
│   ├── bm25-search/            # Lexical search
│   └── contextual-retrieval/   # Advanced retrieval
├── 06-advanced-features/      # Claude's advanced capabilities
│   ├── extended-thinking/      # Extended reasoning
│   ├── multimodal/            # Image and PDF support
│   ├── citations/             # Source attribution
│   └── prompt-caching/        # Caching optimizations
├── 07-mcp/                   # Model Context Protocol
│   ├── mcp-setup/             # Project setup
│   ├── tools-definition/      # Defining tools
│   ├── resources/             # Resource management
│   └── prompts/               # Prompt definitions
├── 08-anthropic-apps/        # Claude Code and Computer Use
│   ├── claude-code/           # Code generation
│   ├── computer-use/          # GUI automation
│   └── debugging/             # Automated debugging
├── 09-agents-workflows/      # Building AI agents
│   ├── parallelization/       # Parallel workflows
│   ├── chaining/              # Sequential workflows
│   ├── routing/               # Decision-based routing
│   └── environment/           # Environment inspection
├── final-project/            # Capstone project
└── docs/                     # Documentation and notes
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