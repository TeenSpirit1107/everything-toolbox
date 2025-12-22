#!/bin/bash
# Function to ask for user confirmation
confirm() {
    read -rp "$1 [y/N]: " response
    case "$response" in
        [yY][eE][sS]|[yY]) true ;;
        *) false ;;
    esac
}

# Function to get free space in KB
get_free_kb() {
    df --output=avail / | tail -n 1
}

echo "==== System Cleaner for Ubuntu ===="
echo "==== Author: Yimeng (Rosalind) ===="
echo "==== Github Profile: https://github.com/TeenSpirit1107 ===="
echo "==== Email: yimengteng@link.cuhk.edu.cn ===="

# Initialize an associative array to store space saved
declare -A space_saved
total_before=$(get_free_kb)

# 1. Clear user cache
if confirm "Do you want to delete user cache files (rm -rf ~/.cache/*)?"; then
    before=$(get_free_kb)
    rm -rf ~/.cache/*
    after=$(get_free_kb)
    space_saved["User cache"]=$((after - before))
    echo "User cache cleared."
else
    space_saved["User cache"]=0
    echo "Skipped cache cleanup."
fi

# 2. apt-get clean & autoremove
if confirm "Do you want to clean apt cache and remove unnecessary packages (apt-get clean, autoremove)?"; then
    before=$(get_free_kb)
    sudo apt-get clean
    sudo apt-get autoremove -y
    after=$(get_free_kb)
    space_saved["APT cleanup"]=$((after - before))
    echo "APT cache cleaned and unused packages removed."
else
    space_saved["APT cleanup"]=0
    echo "Skipped apt cleanup."
fi

# 3. Clean system logs older than 7 days
if confirm "Do you want to clean system logs older than 7 days?"; then
    before=$(get_free_kb)
    sudo find /var/log -type f -name "*.log" -mtime +7 -exec rm -f {} \;
    after=$(get_free_kb)
    space_saved["Log cleanup"]=$((after - before))
    echo "Old system logs deleted."
else
    space_saved["Log cleanup"]=0
    echo "Skipped log cleanup."
fi

# 4. Clean conda cache
if command -v conda &> /dev/null; then
    if confirm "Do you want to clean the conda package cache?"; then
        before=$(get_free_kb)
        conda clean --all --yes
        after=$(get_free_kb)
        space_saved["Conda cleanup"]=$((after - before))
        echo "Conda cache cleaned."
    else
        space_saved["Conda cleanup"]=0
        echo "Skipped conda cleanup."
    fi
else
    space_saved["Conda cleanup"]=0
    echo "Conda is not installed. Skipping conda cache cleanup."
fi

# Final space stats
total_after=$(get_free_kb)
total_saved=$((total_after - total_before))

echo ""
echo "==== Cleanup Summary ===="
for key in "${!space_saved[@]}"; do
    kb=${space_saved[$key]}
    printf "%-20s: %.2f MB\n" "$key" "$(bc <<< "$kb/1024")"
done
echo "----------------------------"
printf "Total space saved : %.2f MB\n" "$(bc <<< "$total_saved/1024")"
echo "============================"


