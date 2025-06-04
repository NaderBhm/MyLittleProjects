import java.util.Random;
import java.util.Scanner;

public class main3 {
    static Random random = new Random();
    public static void main(String[] args){
        Scanner input = new Scanner(System.in);
        int balance=100,amount,result,choice;
        String[] symbols={"🍉","🍎","🍒","🍓","🌶️"};
        System.out.println("####################################");
        System.out.println("# Welcome to the Java Slot Machine #");
        System.out.println("#       Symbols : 🍉🍎🍒🍓🌶️      #");
        System.out.println("####################################");
        do{
            System.out.println("Current balance: $"+balance);
            System.out.print("Place your bet amount: ");
            while((amount=input.nextInt())<=0 || amount>balance){
                System.out.println("Invalid amount");
            }
            balance-=amount;
            System.out.println("spinning");
            result=spin(symbols);
            if(result==0){
                System.out.println("Sorry you lost this round");
            } else if (result==1) {
                System.out.println("You won $"+amount*5);
                balance+=amount*5;
            }
            else{
                System.out.println("Jackpot !!! You won $"+amount*10);
                balance+=amount*10;
            }
            if(balance==0){
                System.out.println("you're out of money 😔");
                break;
            }
            System.out.print("Do you want to continue ?(1 for yes, 0 for no): ");
            while((choice=input.nextInt())!=0 && choice!=1){
                System.out.print("\nPlease choose 1 or 0: ");
            }
        }while(choice!=0);
        System.out.println("Come play again soon!");
        input.close();
    }
    static int spin(String[] symbols){
        int n1,n2,n3;
        n1= random.nextInt(0,5);
        n2= random.nextInt(0,5);
        n3= random.nextInt(0,5);
        System.out.println("**************");
        System.out.printf(" %s | %s | %s \n",symbols[n1],symbols[n2],symbols[n3]);
        System.out.println("**************");
        return (n1==n2?1:0) + (n2==n3?1:0) + (n1==n3?1:0);
    }
}
