#
alias launcher="$(realpath "$(dirname "${BASH_SOURCE}")")/launcher.sh"  # @doc: Shortcut for launcher.sh script
#
alias launcher-inst='launcher ow install && launcher ow wa && redis_ip && echo ""'  # @doc: Install openwhisk using launcher command
#
alias launcher-uninst='launcher ow uninstall'  # @doc: Uninstall openwhisk instation using launcher command
#
alias redis_ip="$(realpath "$(dirname "${BASH_SOURCE}")")/redis_ip.sh"  # @doc: Shortcut for redis_ip.sh script
