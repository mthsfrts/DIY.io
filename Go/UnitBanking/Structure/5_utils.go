package Structure

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"os/exec"
	"runtime"
	"strings"
	"time"
)

var usuarios []Usuario

func EscolherTipoConta() string {
	fmt.Println("Qual tipo de conta você deseja criar?")
	fmt.Println("1. Conta Corrente")
	fmt.Println("2. Conta Poupança")
	fmt.Println("3. Conta Fidelidade")
	fmt.Print("Opção: ")

	var opcao int
	_, err := fmt.Scan(&opcao)
	if err != nil {
		fmt.Println("Erro na leitura do tipo de conta:", err)
		return ""
	}

	switch opcao {
	case 1:
		return TipoContaNormal
	case 2:
		return TipoContaPoupanca
	case 3:
		return TipoContaFidelidade
	default:
		fmt.Println("Opção inválida!")
		return ""
	}
}

func EscolherTipoMovimentacao() string {
	fmt.Println("Qual tipo de movimentação você deseja realizar?")
	fmt.Println("1. Crédito")
	fmt.Println("2. Débito")
	fmt.Println("3. Transferência")
	fmt.Print("Opção: ")

	var opcao int
	_, err := fmt.Scan(&opcao)
	if err != nil {
		fmt.Println("Erro na leitura do tipo de movimentação:", err)
		return ""
	}

	switch opcao {
	case 1:
		return TipoMovimentacaoCredito
	case 2:
		return TipoMovimentacaoDebito
	case 3:
		return TipoMovimentacaoTransferencia
	default:
		fmt.Println("Opção inválida!")
		return ""
	}
}

func Escolhamenu() string {
	var opcao int

	fmt.Println("Deseja Voltar para Menu Principal?")
	fmt.Println("1. Sim")
	fmt.Println("2. Não")
	fmt.Println("Opção :")

	_, err := fmt.Scan(&opcao)
	if err != nil {
		fmt.Println("Erro na Opção:", err)
		return ""
	}

	switch opcao {
	case 1:
		return EscolhaMenuSim
	case 2:
		return EscolhaMenuNao
	default:
		return "Tipo inválido"
	}
}

func ReturnMenu(tipo string) {
	switch tipo {
	case EscolhaMenuSim:
		fmt.Println("Voltando para menu Principal..Aguarde!")
		Wait()
		ClearScreen()

	case EscolhaMenuNao:
		fmt.Println("Ok, esperando proxíma iteração...")
		Wait()
		Escolhamenu()
	}
}

func GerarNumeroConta(tipo string) string {
	rand.Seed(time.Now().UnixNano())
	numero := rand.Intn(9000) + 1000 // Gera um número aleatório entre 1000 e 9999

	switch tipo {
	case TipoContaNormal:
		return fmt.Sprintf("%d-7", numero)
	case TipoContaPoupanca:
		return fmt.Sprintf("%d-8", numero)
	case TipoContaFidelidade:
		return fmt.Sprintf("%d-9", numero)
	default:
		return "Tipo inválido"
	}
}

func PegaNome() []string {
	reader := bufio.NewReader(os.Stdin)

	for {
		fmt.Println("Digite seu nome completo:")
		nome, _ := reader.ReadString('\n') // Lê nome até quebra de linha

		nomeCompleto := strings.Fields(nome) // Divide em campos

		if len(nomeCompleto) < 2 {
			fmt.Println("Nome completo inválido.")
			continue
		} else {
			for i := 0; i < 30; i++ {
				fmt.Print("--")
			}
			fmt.Printf("\nOlá %s, \nBem-vindo ao Banco Unit!\n", nomeCompleto[0]) // Sauda usando o primeiro nome
			usuarios = append(usuarios, Usuario{Nome: strings.Join(nomeCompleto, " ")})
			return nomeCompleto
		}
	}
}

func RandomFloat(min, max float64) float64 {
	return min + rand.Float64()*(max-min)
}

func MostrarMenu() {
	for i := 0; i < 30; i++ {
		fmt.Print("--")
	}
	fmt.Println("\nSelecione uma opção:")
	fmt.Println("1. Criar uma Conta Bancária.")
	fmt.Println("2. Movimentação.")
	fmt.Println("3. Consultar o saldo de uma conta.")
	fmt.Println("4. Consultar o bônus de uma conta fidelidade.")
	fmt.Println("5. Quanto sua conta Poupança está rendendo de juros.")
	fmt.Println("6. Quanto sua conta Fidelidade está rendendo de bônus.")
	fmt.Println("7. Cancelar sua conta.")
	fmt.Println("8. Sumario de conta(s).")
	fmt.Println("0. Sair")
	fmt.Print("Opção: ")
}

func ClearScreen() {
	var cmd *exec.Cmd
	switch runtime.GOOS {
	case "windows":
		cmd = exec.Command("cmd", "/c", "cls")
	case "linux", "darwin": // "darwin" é o nome do GOOS para sistemas MacOS
		cmd = exec.Command("clear")
	default:
		return
	}
	cmd.Stdout = os.Stdout
	err := cmd.Run()
	if err != nil {
		return
	}
}

func Wait() {
	time.Sleep(5 * time.Second)
}
