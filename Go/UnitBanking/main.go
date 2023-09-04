package main

import (
	"UnitBanking/Structure"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

var usuariosContas []Structure.Usuario

func main() {
	lista := Structure.NovaLista()

	fmt.Println("Iniciando Sistema...")
	time.Sleep(1 * time.Second)

	// Chama a função para pegar o nome completo do usuário.
	nomeDoUsuario := Structure.PegaNome() // Mudança aqui para receber o retorno da função

	fmt.Println("Carregando Painel...")
	time.Sleep(3 * time.Second)

	for {
		Structure.MostrarMenu()
		var opcao int
		_, err := fmt.Scan(&opcao)
		if err != nil {
			fmt.Println("Erro ao ler opção:", err)
			return
		}
		switch opcao {
		case 1:
			//Criando Conta
			tipoConta := Structure.EscolherTipoConta()
			if tipoConta == "" {
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
				continue
			}

			acc := Structure.GerarNumeroConta(tipoConta)
			parts := strings.Split(acc, "-")
			numero, _ := strconv.Atoi(parts[0])
			digito, _ := strconv.Atoi(parts[1])

			amount := Structure.RandomFloat(10, 1000)

			// Criar uma conta bancária
			fmt.Println("Criando sua Conta Bancária!")
			conta := lista.InserirContaGeral(numero, digito, amount, tipoConta)
			amountformatted := fmt.Sprintf("%.2f", amount)
			Structure.Wait()
			fmt.Println("Conta Criada! Aqui está o número para acessá-la:", numero, "com dígito", digito)
			fmt.Println("Seu primeiro saque foi de:", amountformatted)

			usuariosContas = append(usuariosContas, Structure.Usuario{
				Nome:   strings.Join(nomeDoUsuario, " "),
				Contas: []*Structure.ContaGeral{conta},
			})
			menu := Structure.Escolhamenu()
			Structure.ReturnMenu(menu)
		case 2:
			//Movimentação
			tipoMovimentacao := Structure.EscolherTipoMovimentacao()

			fmt.Println("Digite o número da conta:")
			var acccheck int
			_, err := fmt.Scan(&acccheck)
			if err != nil {
				fmt.Println("Erro ao ler o número da conta:", err)
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}

			fmt.Println("Digite o dígito da conta:")
			var digcheck int
			_, err = fmt.Scan(&digcheck)
			if err != nil {
				fmt.Println("Erro ao ler o dígito da conta:", err)
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}

			fmt.Println("Buscando Conta!")
			Structure.Wait()

			if !lista.ContaExiste(acccheck, digcheck) {
				fmt.Println("Conta não encontrada, verifique e tente novamente!")
				time.Sleep(1 * time.Second)
				fmt.Println("Voltando para menu Principal..Aguarde!")
				time.Sleep(3 * time.Second)
				Structure.ClearScreen()
				continue
			}

			switch tipoMovimentacao {
			case Structure.TipoMovimentacaoCredito:
				fmt.Println("Agora digite o valor:")
				var amncheck float64
				_, err = fmt.Scan(&amncheck)
				if err != nil {
					fmt.Println("Erro ao ler o valor:", err)
					menu := Structure.Escolhamenu()
					Structure.ReturnMenu(menu)
				}
				lista.Movimentacao(acccheck, digcheck, amncheck, "credito", 0, 0)
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)

			case Structure.TipoMovimentacaoDebito:
				fmt.Println("Agora digite o valor a ser debitado:")
				var amncheck float64
				_, err = fmt.Scan(&amncheck)
				if err != nil {
					fmt.Println("Erro ao ler o valor:", err)
					menu := Structure.Escolhamenu()
					Structure.ReturnMenu(menu)
				}
				lista.Movimentacao(acccheck, digcheck, amncheck, "debito", 0, 0)
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)

			case Structure.TipoMovimentacaoTransferencia:
				fmt.Println("Agora digite a conta para qual deseja enviar o valor:")
				var accdes, digdes int
				_, err = fmt.Scan(&accdes)
				if err != nil {
					fmt.Println("Erro ao ler o número da conta de destino:", err)
					menu := Structure.Escolhamenu()
					Structure.ReturnMenu(menu)

				}
				fmt.Println("Digite o dígito da conta de destino:")
				_, err = fmt.Scan(&digdes)
				if err != nil {
					fmt.Println("Erro ao ler o dígito da conta de destino:", err)
					menu := Structure.Escolhamenu()
					Structure.ReturnMenu(menu)

				}

				fmt.Println("Digite o valor que deseja transferir:")
				var amncheck float64
				_, err = fmt.Scan(&amncheck)
				if err != nil {
					fmt.Println("Erro ao ler o valor:", err)
					menu := Structure.Escolhamenu()
					Structure.ReturnMenu(menu)

				}

				contaOrigem := lista.Buscar(acccheck, digcheck)
				if contaOrigem.Saldo() < amncheck {
					fmt.Println("Saldo insuficiente na conta de origem.")
					menu := Structure.Escolhamenu()
					Structure.ReturnMenu(menu)

				}
				fmt.Println("Realizando Tranferência")
				Structure.Wait()
				fmt.Println("Tranferência Concluida com Sucesso")
				lista.Movimentacao(acccheck, digcheck, amncheck, "transferencia", accdes, digdes)
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}
			continue

		case 3:
			// Consultar o saldo
			fmt.Println("Digite o número da conta consultar o Saldo:")

			var acccheck int
			_, err := fmt.Scan(&acccheck)
			if err != nil {
				fmt.Println("Erro ao ler o número da conta:", err)
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}

			// Solicitando o dígito da conta
			fmt.Println("Digite o dígito da conta:")
			var digcheck int
			_, err = fmt.Scan(&digcheck)
			if err != nil {
				fmt.Println("Erro ao ler o dígito da conta:", err)
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}

			// Buscando a conta
			fmt.Println("Buscando Conta!")
			Structure.Wait()

			amount := lista.ConsultarSaldo(acccheck, digcheck)
			amountformatted := fmt.Sprintf("%.2f", amount)
			fmt.Println("Buscando Saldo da Conta.")
			Structure.Wait()
			fmt.Println("Saldo da Conta é:", amountformatted)
			menu := Structure.Escolhamenu()
			Structure.ReturnMenu(menu)

		case 4:
			// Consultar o bônus de uma conta fidelidade
			fmt.Println("Digite o número da sua Conta Fidelidade:")

			var acc int
			_, err := fmt.Scan(&acc)
			if err != nil {
				fmt.Println("Erro ao ler o número da conta:", err)
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}

			fmt.Println("Digite o dígito da sua Conta Fidelidade:")
			var dig int
			_, err = fmt.Scan(&dig)
			if err != nil {
				fmt.Println("Erro ao ler o dígito da conta:", err)
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}

			// Verificando se o dígito da conta corresponde a uma conta fidelidade
			if dig != 9 {
				fmt.Println("Conta não é uma Conta Fidelidade.")
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}

			bonus := lista.ConsultarBonus(acc, dig) // Ajustado para considerar o dígito
			bonusformatted := fmt.Sprintf("%.2f", bonus)
			fmt.Println("Buscando Bônus da Conta.")
			Structure.Wait()
			fmt.Println("Bônus da Conta é:", bonusformatted)
			menu := Structure.Escolhamenu()
			Structure.ReturnMenu(menu)

		case 5:
			// Render juros de uma conta poupança
			fmt.Printf("Buscando Conta(s) Poupança...\n")
			time.Sleep(3 * time.Second)
			if lista.IsEmpty() {
				fmt.Printf("Nenhuma Poupança cadastrada para o usuario...\n")
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}
			// Função modificada para renderizar juros apenas para contas poupança
			curr := lista.Head
			for curr != nil {
				if cp, ok := curr.Conta.(*Structure.ContaGeral); ok && cp.Tipo() == "POUPANCA" {
					juros := cp.Render()
					fmt.Printf("Juro rendendo para a conta %d-%d. Valor do juros: %.2f\n", cp.Numero, cp.Digito, juros)
					menu := Structure.Escolhamenu()
					Structure.ReturnMenu(menu)
				} else {
					fmt.Printf("A conta %d-%d não é uma conta poupança e, portanto, não recebe juros..\n", curr.Conta.Numero(), curr.Conta.Digito())
					fmt.Printf("Escolha a Opçâo 1 do Menu Iterativo para criar sua Conta Poupança.")
					menu := Structure.Escolhamenu()
					Structure.ReturnMenu(menu)
				}
				curr = curr.Next
			}

		case 6:
			//
			fmt.Printf("Buscando Conta(s) Fidelidade...\n")
			time.Sleep(3 * time.Second)
			if lista.IsEmpty() {
				fmt.Printf("Nenhuma Fidelidade cadastrada para o usuario...\n")
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}
			// Função modificada para renderizar juros apenas para contas poupança
			curr := lista.Head
			for curr != nil {
				if cp, ok := curr.Conta.(*Structure.ContaGeral); ok && cp.Tipo() == "FIDELIDADE" {
					juros := cp.Render()
					fmt.Printf("Juro rendendo para a conta %d-%d. Valor do juros: %.2f\n", cp.Numero, cp.Digito, juros)
					menu := Structure.Escolhamenu()
					Structure.ReturnMenu(menu)
				} else {
					fmt.Printf("A conta %d-%d não é uma conta poupança e, portanto, não recebe juros.\n", curr.Conta.Numero(), curr.Conta.Digito())
					fmt.Printf("Escolha a Opçâo 1 do Menu Iterativo para criar sua Conta Fidelidade.")
					menu := Structure.Escolhamenu()
					Structure.ReturnMenu(menu)
				}
				curr = curr.Next
			}

		case 7:
			// Remover uma conta
			fmt.Println("Qual o numero da sua conta?")
			var acc int
			_, err = fmt.Scan(&acc)
			if err != nil {
				fmt.Println("Erro ao ler o número da conta:", err)
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}

			fmt.Println("Digite o dígito da sua conta:")
			var dig int
			_, err = fmt.Scan(&dig)
			if err != nil {
				fmt.Println("Erro ao ler o dígito da conta:", err)
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}

			// Verificando se a conta existe
			if !lista.ContaExiste(acc, dig) {
				fmt.Println("Conta não encontrada. Verifique o número e o dígito e tente novamente.")
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}

			lista.Remover(acc, dig) // Ajustado para considerar o dígito
			fmt.Println("Cancelando Conta...Espere!")
			Structure.Wait()
			fmt.Println("Conta Cancelada!")
			menu := Structure.Escolhamenu()
			Structure.ReturnMenu(menu)

		case 8:
			fmt.Println("Buscando todas as contas")
			time.Sleep(3 * time.Second)
			// Imprimir número e saldo de todas as contas cadastradas
			if !lista.Imprimir() {
				fmt.Println("Nenhuma conta vinculada ao seu usuário!")
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			} else {
				menu := Structure.Escolhamenu()
				Structure.ReturnMenu(menu)
			}

		case 0:
			fmt.Println("Saindo...")
			Structure.Wait()
			fmt.Printf("Até Logo %v...", nomeDoUsuario[0])
			Structure.ClearScreen()
			os.Exit(0)

		default:
			fmt.Println("Opção inválida!")
			menu := Structure.Escolhamenu()
			Structure.ReturnMenu(menu)
		}
	}
}
