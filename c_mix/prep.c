# include <stdio.h>
# include <string.h>
# include <stdlib.h>

struct pingRecord {
  double coords[3];
  char desc[200];
};

int main()
{    
    FILE *inPointer; 
    FILE *outPointer; 
    
    inPointer = fopen("to-c.csv", "r");
    outPointer = fopen("proced", "wb");

    char line[500];
    struct pingRecord record;
    int i, c, ei;
    char elem[500];
    char v;
    memset(elem, 0, sizeof(elem));

    int l = -1;
    while(fgets(line, 500, inPointer) != NULL)
    {
        l++;
        c = 1; i = 0; ei = 0;
        while(1){
            v = line[i];
            i++;
            if( (v == ';') | (v == '\n')){
                //elem done
                if ( c < 4){
                    record.coords[c - 1] = strtod(elem, NULL); //atof(elem); //strtod(elem, NULL);
                }else{
                    strcpy(record.desc, elem);
                }
                c++; ei=0;
                memset(elem, 0, sizeof(elem));
                if (v == '\n'){
                    fwrite(&record, sizeof(struct pingRecord), 1, outPointer);
                    memset(record.desc, 0, sizeof(record.desc));
                    break;
                }
            }else{
                elem[ei] = v;
                ei++;
            }
        }
    }
    fclose(inPointer);
    fclose(outPointer);
    return 0;       
}