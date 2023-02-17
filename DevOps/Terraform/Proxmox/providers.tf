terraform {

  required_version = ">= 0.13.0"

  required_providers {

    proxmox = {
      source  = "telmate/proxmox"
      version = "2.9.11"
    }
    # If want to you vault to pass all your secret keys, uncomment the following code.
      
    # vault = {
    #   source = "hashicorp/vault"
    #   version = "3.12.0"
    # }
  }
}

provider "proxmox" {

  pm_api_url          = var.proxmox["url"]
  pm_api_token_id     = var.proxmox["id"]
  pm_api_token_secret = var.proxmox["key"]
  pm_tls_insecure     = true
}

# provider "vault" {
#   address = "VAULT-ADDRESS"
#   token   = "VAULT-ACCESS-TOKEN"
# }