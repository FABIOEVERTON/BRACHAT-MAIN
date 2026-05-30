if not contains "$HOME/brachat-main/.data/../bin" $PATH
    # Prepending path in case a system-installed binary needs to be overridden
    set -x PATH "$HOME/brachat-main/.data/../bin" $PATH
end
