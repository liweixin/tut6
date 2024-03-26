#include <stdio.h>
#include <string.h>

void unsafe_copy(char *input_str)
{
    char target_str[100];

    // !!!buffer overflowing here
    strcpy(target_str, input_str);

    /* Debug Tool: Uncomment the following codes to directly get the needed address info.
        Please refer to the following sites for details.
        1) "https://www.cristal.univ-lille.fr/~marquet/ens/ctx/doc/l-ia.html"
        2) "https://dmalcolm.fedorapeople.org/gcc/2015-08-31/rst-experiment/how-to-use-inline-assembly-language-in-c-code.html#defining-global-register-variables"
    */

    register char *ebp asm("ebp");
    printf("address of target_str is %p\n", &target_str); // %p means hex
    printf("address of ebp is %p\n", ebp);
}

int main()
{
    char input_str[500];
    FILE *badfile;
    badfile = fopen("badfile", "r");
    fread(input_str, sizeof(char), 200, badfile);
    unsafe_copy(input_str);
    printf("Return properly!\n");
    return 1;
}
