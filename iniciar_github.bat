@echo off
echo ========================================
echo 🚀 INICIANDO REPOSITORIO GITHUB ACTIONS
echo ========================================
echo.

echo 📁 Verificando estrutura de arquivos...
if not exist "scraper.py" (
    echo ❌ ERRO: scraper.py nao encontrado!
    echo Execute este script da pasta meu-scraper/
    pause
    exit /b 1
)

if not exist ".github\workflows\scraper.yml" (
    echo ❌ ERRO: Workflow do GitHub Actions nao encontrado!
    echo Execute este script da pasta meu-scraper/
    pause
    exit /b 1
)

echo ✅ Estrutura de arquivos OK!
echo.

echo 🔧 Inicializando repositorio Git...
git init
if %errorlevel% neq 0 (
    echo ❌ ERRO: Falha ao inicializar Git
    pause
    exit /b 1
)

echo ✅ Git inicializado!
echo.

echo 📝 Adicionando arquivos...
git add .
if %errorlevel% neq 0 (
    echo ❌ ERRO: Falha ao adicionar arquivos
    pause
    exit /b 1
)

echo ✅ Arquivos adicionados!
echo.

echo 💾 Fazendo primeiro commit...
git commit -m "🚀 Inicializar scraper FAPEMIG automatizado"
if %errorlevel% neq 0 (
    echo ❌ ERRO: Falha ao fazer commit
    pause
    exit /b 1
)

echo ✅ Commit realizado!
echo.

echo 🌿 Configurando branch main...
git branch -M main
if %errorlevel% neq 0 (
    echo ❌ ERRO: Falha ao configurar branch
    pause
    exit /b 1
)

echo ✅ Branch main configurada!
echo.

echo.
echo ========================================
echo 📋 PROXIMOS PASSOS:
echo ========================================
echo.
echo 1. Crie um repositorio no GitHub
echo 2. Execute o comando abaixo (substitua a URL):
echo.
echo    git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
echo.
echo 3. Execute:
echo.
echo    git push -u origin main
echo.
echo 4. Configure os secrets no GitHub:
echo    - EMAIL_USER: seu email Gmail
echo    - EMAIL_PASS: senha de app do Gmail
echo.
echo 5. Verifique a primeira execucao automatica
echo.
echo ========================================
echo.

echo 🧪 Quer testar o scraper localmente primeiro?
set /p resposta="Digite 's' para sim ou Enter para nao: "
if /i "%resposta%"=="s" (
    echo.
    echo 🚀 Executando teste local...
    python teste_local.py
    echo.
    echo Pressione qualquer tecla para continuar...
    pause >nul
)

echo.
echo ✅ Repositorio inicializado com sucesso!
echo.
pause
