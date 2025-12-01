.PHONY: swap

swap:
	@if [ -z "$(filter-out swap,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make swap <size>"; \
		echo "Example: make swap 16gb"; \
		exit 1; \
	fi
	@SIZE=$(filter-out swap,$(MAKECMDGOALS)); \
	echo "Creating swap file of size $$SIZE..."; \
	sudo dd if=/dev/zero of=/swapfile bs=1M count=$$(echo $$SIZE | sed 's/gb/*1024/i' | bc) status=progress && \
	sudo chmod 600 /swapfile && \
	sudo mkswap /swapfile && \
	sudo swapon /swapfile && \
	echo "Swap file created and activated successfully"

# Catch-all target to handle size argument
%:
	@:
