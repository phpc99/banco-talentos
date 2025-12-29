# Video

You can watch the video showcasing the project in the following links:
- [Version 1](https://youtu.be/iBGr6hU_tPM). Also available on branch _version1_;
- Version 2: soon

# How to Run the Project

Follow these steps to run this Django project on your machine.

## 1. **Clone the repository**

`git clone https://github.com/phpc99/banco-talentos.git`

## 2. **Create a virtual environment**

`python -m venv venv` 

## 3. **Activate the virtual environment**

### Windows (PowerShell or CMD):

`venv\Scripts\activate` 

### macOS / Linux:

`source venv/bin/activate` 

You should now see `(venv)` at the start of your terminal prompt.

## 4. **Install dependencies**

`pip install -r requirements.txt` 

## 5. **Change the directory**

`cd banco_talentos`

## 6. **Apply migrations**

`python manage.py migrate` 

## 7. **Run the development server**

`python manage.py runserver` 

## 8. **Open the website**

Go to: http://127.0.0.1:8000/

'Gestor' role credentials:
- user: _gestor_
- password: _1234_

# _EN_ Features of version 2

## Candidates

- Candidate registration with personal data, education level, desired position, and résumé/photo upload
- Public consultation of application status via email
- Simple and intuitive flow to participate in the Talent Pool

## Application Management (Manager Dashboard)

- Administrative dashboard to view and manage all applications
- Filters by state, education level, and job area
- Real-time application status updates
- Application deletion with confirmation modal
- Internal notes system per candidate
- Paginated results for better performance and usability

## Data Visualization

- Dynamic charts (bar and pie) to analyze candidates by: Area, Education, and State
- Chart type switching directly in the interface
- Responsive layout consistent with the administrative dashboard

## Interviews

- Dedicated list of candidates selected for interviews
- Complete interview workflow with: Common questionnaire and Area-specific questionnaire
- Evaluation with scores and observations
- Final interview decision options: Approved, Rejected, No-show, In progress (decide later)
- Ability to review completed interviews
- Interview deletion with confirmation
- Visual feedback for interview status (“Interview completed”)

## Institutional Pages

- Careers page with detailed descriptions for each role
- Tab-based navigation between career paths
- Call-to-action (CTA) for Talent Pool registration
- Home page with hero section and embedded institutional video

## UI / UX

- Consistent design across public and administrative pages
- Reusable cards, standardized spacing, and uniform typography
- Confirmation modals for sensitive actions
- Success messages and visual feedback for manager actions

## Security & Access Control

- Protected administrative area for managers
- Clear separation between public (candidate) and internal (manager) workflows

# _PT_ Features da versão 2

## Candidatos

- Cadastro de candidatos com dados pessoais, formação, área pretendida e upload de currículo/foto
- Consulta pública do status da candidatura via e-mail
- Fluxo simples e intuitivo para participação no Banco de Talentos

## Gestão de Candidaturas (Painel do Gestor)

- Painel administrativo para visualização e gestão de todas as candidaturas
- Filtros por estado, formação e área
- Atualização de status da candidatura em tempo real
- Exclusão de candidaturas com confirmação via modal
- Sistema de anotações internas por candidato
- Paginação de resultados para melhor desempenho e usabilidade

## Visualização de Dados

- Gráficos dinâmicos (barras e pizza) para análise de candidatos por: Área, Formação, Estado
- Alternância de tipo de gráfico diretamente na interface
- Layout responsivo e consistente com o painel administrativo

## Entrevistas

- Lista dedicada de candidatos selecionados para entrevista
- Fluxo completo de entrevista com: questionário comum e específico por área
- Avaliação com notas e observações
- Decisão final da entrevista: Aprovado, Reprovado, Não compareceu, Em andamento (decidir depois)
- Possibilidade de rever entrevistas já realizadas
- Exclusão de entrevistas com confirmação
- Feedback visual de status (“Já foi entrevistado”)

## Páginas Institucionais

- Página de carreiras com descrição detalhada de cada cargo
- Navegação por tabs entre carreiras
- CTA para cadastro no Banco de Talentos
- Home page com seção hero e vídeo institucional incorporado

## UI / UX

- Design consistente entre páginas públicas e administrativas
- Cards reutilizáveis, espaçamentos padronizados e tipografia uniforme
- Modais de confirmação para ações sensíveis
- Mensagens de sucesso e feedback visual para ações do gestor

## Segurança & Controle de Acesso

- Área administrativa protegida para gestores
- Separação clara entre fluxo público (candidato) e interno (gestor)
