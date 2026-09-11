#!/usr/bin/env bash
# ==============================================================================
# PROJECT COMMAND CENTER: ez_grav / agy-workspace
# Refactored for User-Friendliness & Idempotency
# ==============================================================================
set -u

# --- Configuration ---
PROJECT_NAME="ez_grav"
VENV_DIR=".venv"
REQ_FILE="requirements.txt"
LOG_DIR="logs"
DOCS_DIR="docs"
SRC_DIR="src"
TEST_DIR="tests"

# Colors for user-friendliness
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- Utility Functions ---
log_info() { printf "${BLUE}[INFO]${NC} %s\n" "$1"; }
log_success() { printf "${GREEN}[SUCCESS]${NC} %s\n" "$1"; }
log_warn() { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; }
log_error() { printf "${RED}[ERROR]${NC} %s\n" "$1"; }

check_cmd() {
    command -v "$1" >/dev/null 2>&1 || { log_error "$1 is required but not installed."; exit 1; }
}

# --- Module: Environment Setup ---
setup_env() {
    log_info "Initializing environment..."
    
    # Idempotent directory creation
    for dir in "$LOG_DIR" "$DOCS_DIR" "$SRC_DIR" "$TEST_DIR"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_info "Created directory: $dir"
        fi
    done

    # Python Virtual Env Setup
    if [ ! -d "$VENV_DIR" ]; then
        log_info "Creating virtual environment in $VENV_DIR..."
        python3 -m venv "$VENV_DIR"
        log_success "Virtual environment created."
    else
        log_info "Virtual environment already exists. Skipping."
    fi

    # Install Dependencies
    if [ -f "$REQ_FILE" ]; then
        log_info "Installing dependencies from $REQ_FILE..."
        "$VENV_DIR/bin/pip" install --upgrade pip > /dev/null
        "$VENV_DIR/bin/pip" install -r "$REQ_FILE" > /dev/null
        log_success "Dependencies installed."
    else
        log_warn "$REQ_FILE not found. No packages installed."
    fi
}

# --- Module: Git & OPSEC Health Check ---
health_check() {
    log_info "Running system health check..."
    
    # Git check
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        STATUS=$(git status --short)
        if [ -z "$STATUS" ]; then
            log_success "Git: Workspace clean."
        else
            log_warn "Git: Uncommitted changes detected."
        fi
    else
        log_error "Git: Not a git repository."
    fi

    # File permission check (OPSEC)
    if [ -f "ez_grav.py" ]; then
        PERMS=$(stat -c "%a" "ez_grav.py")
        if [ "$PERMS" -gt "600" ]; then
            log_warn "OPSEC: ez_grav.py has loose permissions ($PERMS). Consider chmod 600."
        else
            log_success "OPSEC: ez_grav.py permissions are secure."
        fi
    fi
}

# --- Module: Testing ---
run_all_tests() {
    log_info "Launching test suite..."
    if [ -f "run_tests.sh" ]; then
        bash run_tests.sh
    elif [ -f "test_ez_grav.py" ]; then
        "$VENV_DIR/bin/python3" test_ez_grav.py
    else
        log_error "No test entry point found (run_tests.sh or test_ez_grav.py)."
    fi
}

# --- Interactive Menu ---
show_menu() {
    clear
    echo -e "${BLUE}==============================================${NC}"
    echo -e "   ${YELLOW}Project Command Center: $PROJECT_NAME${NC}"
    echo -e "${BLUE}==============================================${NC}"
    echo -e "1) ${GREEN}Full Setup${NC} (Env, Venv, Deps)"
    echo -e "2) ${GREEN}Health Check${NC} (Git, OPSEC, Perms)"
    echo -e "3) ${GREEN}Run Tests${NC}"
    echo -e "4) ${GREEN}Clean Logs${NC}"
    echo -e "5) ${RED}Exit${NC}"
    echo -e "${BLUE}----------------------------------------------${NC}"
    printf "Choose an option: "
}

# --- Main Execution ---
main() {
    check_cmd python3
    check_cmd git

    while true; do
        show_menu
        read -r opt
        case $opt in
            1) setup_env ;;
            2) health_check ;;
            3) run_all_tests ;;
            4) rm -rf "$LOG_DIR"/* && log_success "Logs cleared." ;;
            5) log_info "Quacking out! Goodbye."; exit 0 ;;
            *) log_error "Invalid option." ;;
        esac
        echo -e "\nPress enter to return to menu..."
        read -r
    done
}

main "$@"
