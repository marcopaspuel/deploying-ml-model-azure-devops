provider "azurerm" {
  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name  = "eqr-tf-storage-account-rg"
    storage_account_name = "tstate2836"
    container_name       = "tstate"
    key                  = "terraform.tfstate"
  }
}

module "resource_group" {
  source               = "../../modules/resource_group"
  resource_group       = var.resource_group
  location             = var.location
  project              = var.project
}

module "appservice" {
  source           = "../../modules/appservice"
  location         = var.location
  webapp_name      = var.webapp_name
  resource_type    = "AppService"
  resource_group   = module.resource_group.resource_group_name
  project          = var.project
}
