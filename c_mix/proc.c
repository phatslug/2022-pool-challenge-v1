# include <stdio.h>
# include <string.h>
# include <stdlib.h>

struct pingRecord {
  double coords[3];
  char desc[200];
};

int addPoints(FILE *filePointer, double pointArray[][3]){
    int lineLen = 200;
    char line[lineLen];
    char elem[50];
    memset(elem, 0, sizeof(elem));

    char v;
    int c, i, ei, incount;
    incount = 0; c = 0; ei = 0;

    while(fgets(line, lineLen, filePointer) != NULL){
        i = 0;
        while(1){
            v = line[i];
            i++;
            if ( (i >= lineLen) | (v == ']') )
              break;
            if ( ((v == ',') & (ei > -1)) | (v == '}') ){
                pointArray[incount][c] = strtod(elem, NULL);
                ei=-1;
                c = (c + 1) % 3;
                if (c == 0)
                    incount++;
            }
            if ( (ei > -1) & (v != ' ')){
                elem[ei] = v;
                ei++;
            }
            if(v == ':'){
                ei=0;
                memset(elem, 0, sizeof(elem));
            }
        }
    }
    return incount;
}

int addOutStrings(FILE *filePointer, double inPoints[][3], char outStrings[][200], int incount){
    int i;
    double dist;
    double minDists[5000];
    for (i=0; i<5000; i++)
        minDists[i] = 3.0e+38;

    struct pingRecord record;

    int l = -1;
    while(fread(&record, sizeof(struct pingRecord), 1, filePointer)){
        l++;
        for(i=0; i < incount; ++i){
            dist = (inPoints[i][0] - record.coords[0]) * (inPoints[i][0] - record.coords[0]) + 
            (inPoints[i][1] - record.coords[1]) * (inPoints[i][1] - record.coords[1]) + 
            (inPoints[i][2] - record.coords[2]) * (inPoints[i][2] - record.coords[2]);
            if(dist < minDists[i]){
                minDists[i] = dist;
                strcpy(outStrings[i], record.desc);
            }
        }
    }


    return 0;
}

int main()
{
    FILE *dataPointer; 
    FILE *inPointer; 
    FILE *outPointer; 

    dataPointer = fopen("proced", "rb");
    inPointer = fopen("input.json", "r");
    outPointer = fopen("output.json", "w");


    char outDicts[5000][200];
    double inPoints[5000][3];

    int incount = addPoints(inPointer, inPoints);
    addOutStrings(dataPointer, inPoints, outDicts, incount);

    fputs("[", outPointer);
    for(int i=0; i < incount; ++i){
            fputs(outDicts[i], outPointer);
            if ( (i + 1) < incount)
                fputs(",", outPointer);
        }
    fputs("]", outPointer);
    fclose(dataPointer);
    fclose(inPointer);
    fclose(outPointer);
    return 0;

}