/*---------------Recursive descent compiler ---------------------*/

#  include <stdio.h>
#  include <ctype.h>
#  include <string.h>

/*-------------- Limits ------------------------------------------*/

#define VAR_MAX        100
#define CONST_MAX      100
#define TOKEN_MAX      500
#define PROGRAM_MAX    500

/*void SkipCounter( FILE* ); */

/*--------------------- Types Definition --------------------------*/

/* BOOL */
typedef enum
   {
   FALSE,
   TRUE
   }
   BOOL;

typedef enum
  {
        BEGIN,                 /* Reserved words */
        END,
        IF,
        THEN,
        ELSE,
        FI,
        WHILE,
        DO,
        OD,
        READ,
        WRITE,

	IDENTIFIER,
	CONST,
	LEFT_BRACKET,		/*   ( */
	RIGHT_BRACKET,		/*   ) */
        ADD_SUB,                /*   +,- */
        MULT_DIV,               /*   *,/ */
	RELATION,		/*   >,<,=,!=, ... */
	ASSIGN,			/*   :=  */
        SEMICOLON               /*   ;   */
  }
   TTokenType;
/* Relations :
   =  -  0
   != -  1
   <  -  2
   >  -  3
   <= -  4
   >= -  5   */

typedef struct
  {
      TTokenType TokenType;
      unsigned   Number;
  }
   TToken;

typedef enum
   {
      STOP,
      LOAD,
      STORE,
      INVERT,
      ADD,
      SUB,
      MULT,
      DIV,
      COMPARE,
      JUMP,
      JUMP_YES,
      JUMP_NO,
      INPUT,
      PRINT
   }
   TOperation;   /* Stack machine operations */

typedef struct
  {
      TOperation  Operation;
      unsigned    Address;
  }
   TCommand;     /* Stack machine commands */


/*--------------------------  Tables ----------------------------*/

TToken TOKENS[ TOKEN_MAX ];      /* input program as a sequence of tokens */
unsigned TokenCounter = 0;

int VARIABLES[ VAR_MAX ];        /* Table of program variables */
unsigned NumberOfVariables = 0;

int CONSTANTS[ CONST_MAX ];
unsigned NumberOfConstants = 0;   /* Table of program constants */

TCommand OUTPUT_PROGRAM[ PROGRAM_MAX ]; /* Resulting program for stack 
                                           machine */
unsigned ProgramCounter = 0;

/*-------------------------- String - code pairs (for printing) ---------*/

struct
  {
  char*      Name;
  TTokenType Type;
  }
  RESERVED_WORDS[] =
  {
    { "BEGIN", BEGIN },
    { "END",   END   },
    { "IF",    IF    },
    { "THEN",  THEN  },
    { "ELSE",  ELSE  },
    { "FI",    FI    },
    { "WHILE", WHILE },
    { "DO",    DO    },
    { "OD",    OD    },
    { "READ",  READ  },
    { "WRITE", WRITE }
  };
int ReservedWordsNumber = sizeof( RESERVED_WORDS ) / sizeof( RESERVED_WORDS[0] );

struct
  {
  char*      Name;
  TTokenType Type;
  }
  TOKEN_TYPES[] =
  {
    { "BEGIN",      BEGIN      },
    { "END",        END        },
    { "IF",         IF         },
    { "THEN",       THEN       },
    { "ELSE",       ELSE       },
    { "FI",         FI         },
    { "WHILE",      WHILE      },
    { "DO",         DO         },
    { "OD",         OD         },
    { "READ",       READ       },
    { "WRITE",      WRITE      },
    { "IDENTIFIER", IDENTIFIER },
    { "CONST",      CONST      },
    { "L_BRACKET",  LEFT_BRACKET  },
    { "R_BRACKET",  RIGHT_BRACKET  },
    { "ADD_SUB",    ADD_SUB    },
    { "MULT_DIV",   MULT_DIV   },
    { "RELATION",   RELATION   },
    { "ASSIGN",     ASSIGN     },
    { "SEMICOLON",  SEMICOLON  }
  };
int TokenTypesNumber    = sizeof(  TOKEN_TYPES   ) / sizeof( TOKEN_TYPES[0] );

struct
  {
  char*      Name;
  TOperation Operation;
  }
  SM_OPERATIONS[] =
  {
     { "STOP",    STOP    },
     { "LOAD",    LOAD    },
     { "STORE",   STORE   },
     { "INVERT",  INVERT  },
     { "ADD",     ADD     },
     { "SUB",     SUB     },
     { "MULT",    MULT    },
     { "DIV",     DIV     },
     { "COMPARE", COMPARE },
     { "JUMP",    JUMP    },
     { "JUMP_YES",JUMP_YES},
     { "JUMP_NO", JUMP_NO },
     { "INPUT",   INPUT   },
     { "PRINT",   PRINT   }
  };
int SMOperationsNumber  = sizeof(  SM_OPERATIONS ) / sizeof( SM_OPERATIONS[0] );

/*---------------------  Lex Analyser ----------------------------*/
void Error(const char *);
void Alarm(const char *);
void SkipComment( FILE* );
const char* SourceFileName;
/*const int MaxIdLength = 10; */
#define MaxIdLength (10)

char IDENTIFIERS[ VAR_MAX ][ MaxIdLength + 1 ];
int IdentifiersCount = 0;
void SkipComment( FILE *fp )
  {
    int c;
    c = fgetc( fp );
    do{
    while( !feof( fp ) && ( c != '*' ) )
     c = fgetc( fp );
    if( feof(fp) ) Error("Crazy comment");
    c = fgetc( fp );
    } while( c != '/' ); 
  }
       
void LexicalAnalyzer()
  {
  int c;
  FILE* fp = fopen( SourceFileName, "rt" );
  if ( !fp ) Error( "Fatal error: Can't open source file" );
  c = fgetc( fp );
  while ( c != EOF )
    {
#ifdef DEBUG
	fprintf(stderr,"Current character is '%c'\n",c);
#endif
    while ( isspace( c ) || ( c == '\n' ) )
      {
#ifdef DEBUG
	fprintf(stderr,"Eating up whitespaces...\n");
#endif 
      c = fgetc( fp );
      if ( c == EOF ) return;
      } ;
      
    if ( isalpha( c ) )
      {
        char Identifier[ MaxIdLength + 1 ];
        int i = 0;
#ifdef DEBUG
	fprintf(stderr,"Alpha encountered\n");
#endif
        do
          {
#ifdef DEBUG
	fprintf(stderr,"Reading temporar string: %c\n",c);
#endif
            if ( i < MaxIdLength ) Identifier[ i++ ] = c;
            c = fgetc( fp );
          }
        while ( isalnum( c ) );
        
        Identifier[ i ] = '\0';
        for ( i = 0; i < ReservedWordsNumber; i++ )
          if ( !strcmp( Identifier, RESERVED_WORDS[i].Name )) break;
        if ( i == ReservedWordsNumber )
          {
             /* Identifier */
             /* Search in identifiers table */
             for ( i = 0; i < IdentifiersCount; i++ )
                if ( !strcmp( Identifier, IDENTIFIERS[i] ) ) break;
             if ( i == IdentifiersCount )
               {
                 /* Not in table */
                  strcpy( IDENTIFIERS[ IdentifiersCount ], Identifier );
                  TOKENS[ TokenCounter ].TokenType = IDENTIFIER;
                  TOKENS[ TokenCounter++ ].Number  = IdentifiersCount++;
                  NumberOfVariables++ ; /* Changed */
               }
             else
               {
                 /* Found in table */
                 TOKENS[ TokenCounter ].TokenType = IDENTIFIER;
                 TOKENS[ TokenCounter++ ].Number  = i;
#ifdef DEBUG
	fprintf(stderr,"IDENTIFIER encountered\n");
#endif 
               }
           }
        else
          {
             /* Reserved word of number i */
             TOKENS[ TokenCounter++ ].TokenType = RESERVED_WORDS[i].Type ; 
#ifdef DEBUG
	fprintf(stderr,"RESERVED WORD encountered\n");
#endif
          }
      }
    else if ( isdigit( c ) )
      {
         int constant = c - '0';
         while ( c = fgetc( fp )  )
          { 
		if( isdigit( c ))
		constant = constant*10 + c - '0';
		else  break;
          }
          TOKENS[ TokenCounter ].TokenType = CONST ;
          CONSTANTS[ NumberOfConstants ] = constant ;
          TOKENS[ TokenCounter++ ].Number = NumberOfConstants++ ;
 #ifdef DEBUG
       fprintf(stderr,"CONSTANT encountered\n");
 #endif 
      }
    else if ( c == ':' )
      {
 #ifdef DEBUG
 	fprintf(stderr,"COLON encountered\n");
 #endif
         c = fgetc( fp );
	 if( c != '=' ) Error("'=' expected in assignment");
	 else
         TOKENS[ TokenCounter++ ].TokenType = ASSIGN ;
 #ifdef DEBUG
 	fprintf(stderr,"It was ASSIGNMENT\n");
 #endif
        c = fgetc( fp );
      }
    else if ( c == ';' )
      {
	 TOKENS[ TokenCounter++ ].TokenType = SEMICOLON ;
	 c = fgetc( fp );
      }
    else if ( c == ')' )
      {
         TOKENS[ TokenCounter++ ].TokenType = RIGHT_BRACKET ; 
         c = fgetc( fp );
      }
    else if ( c == '(' )
      {
         TOKENS[ TokenCounter++ ].TokenType = LEFT_BRACKET ;
         c = fgetc( fp );
      }
    else if ( c == '!' )
      {
         c = fgetc( fp );
         if ( c != '=' ) Error("'=' expected after '!' in relation");
         TOKENS[ TokenCounter ].TokenType = RELATION ;
         TOKENS[ TokenCounter++ ].Number = 1 ;
         c = fgetc( fp );
      }
    else if ( c == '<' )
      {
         c = fgetc( fp );
         if ( c == '=' )
            {
              TOKENS[ TokenCounter ].TokenType = RELATION ;
              TOKENS[ TokenCounter++ ].Number = 4 ;
              c = fgetc( fp );
            }
         else
            {
              TOKENS[ TokenCounter ].TokenType = RELATION ;
              TOKENS[ TokenCounter++ ].Number = 2 ;
            }
      }
    else if ( c == '>' )
      {  
         c = fgetc( fp );
         TOKENS[ TokenCounter ].TokenType = RELATION ;
         if ( c== '=' )
            {
              TOKENS[ TokenCounter++ ].Number = 5 ;
              c = fgetc( fp );
            }
         else
              TOKENS[ TokenCounter++ ].Number = 3 ;    
      }
    else if ( c == '=' )
      {
         c = fgetc( fp );
         TOKENS[ TokenCounter ].TokenType = RELATION ;
         TOKENS[ TokenCounter++ ].Number = 0 ;
      }
    else if ( c == '+' )
      {
         TOKENS[ TokenCounter ].TokenType = ADD_SUB ;
         TOKENS[ TokenCounter++ ].Number = 0 ;
         c = fgetc( fp );
      }
    else if ( c == '-' )
      {
         TOKENS[ TokenCounter ].TokenType = ADD_SUB ;
         TOKENS[ TokenCounter++ ].Number = 1 ;
         c = fgetc( fp );
      }
    else if ( c == '*' )
      {
         TOKENS[ TokenCounter ].TokenType = MULT_DIV ;
         TOKENS[ TokenCounter++ ].Number = 0 ;
         c = fgetc( fp );
      }
    else if ( c == '/' )
      {
         c = fgetc( fp );
         if ( c!= '*' )
            {
               TOKENS[ TokenCounter ].TokenType = MULT_DIV ;
               TOKENS[ TokenCounter++].Number = 1;
            }
         else
          { SkipComment( fp );
         c = fgetc( fp ); }
       } 
       
             
    }
  }

/*---------------------  Synt Analyser ----------------------------*/

void IncreaseOutProgram( TOperation Operation, unsigned Address )
   {
        if( ProgramCounter == PROGRAM_MAX )
             Error( "Too large program" );

	OUTPUT_PROGRAM[ ProgramCounter ].Operation = Operation;
	OUTPUT_PROGRAM[ ProgramCounter ].Address   = Address;
	ProgramCounter++;
	return;
   }

void Program();
void StatementList();
void Statement();
void Conditional();
void Expression();
void Term();
void Primary();
void PrintTokenProgram();
void PrintStackMachineProgram();
void Error(const char *msg)
{
	fprintf(stderr,"ERROR:\n\t%s\n",msg);
	exit(-1);
}
void Alarm(const char *msg)
{
	fprintf(stderr,"WARNING:\n\t%s\n",msg);
}
void Program()
   {
	TTokenType  token_type;
	token_type = TOKENS[ TokenCounter++ ].TokenType;
	if( token_type != BEGIN )
		Error( "Program has to be started from 'BEGIN' " );
#ifdef DEBUG1
	fprintf(stderr,"Program() calls StatementList()\n");
#endif
        StatementList();

	token_type = TOKENS[ TokenCounter++ ].TokenType;
	if( token_type != END )
		Error( "Program has to be ended by 'END' " );

        IncreaseOutProgram( STOP, 0);
        return;
   }

void StatementList()
   {
       TTokenType  token_type;
       while( TRUE )
         {
#ifdef DEBUG1
	fprintf(stderr,"StatementList() calls Statement()\n");
#endif
            Statement();
            token_type = TOKENS[ TokenCounter ].TokenType;
            if( token_type != SEMICOLON ) break;
            TokenCounter++;
         }
      return;
   }

void Statement()
   {
	TTokenType token_type;
	unsigned   address;
	unsigned   A1;
	unsigned   A2;

	token_type = TOKENS[ TokenCounter++ ].TokenType;
#ifdef DEBUG1
       fprintf(stderr,"%d\n",token_type);
#endif
	if( token_type == WRITE )
	   {
#ifdef DEBUG1
      fprintf(stderr,"WRITE recognized\n");
#endif
/* Was changed */
                if ( TOKENS[ TokenCounter++ ].TokenType != LEFT_BRACKET)
                   Error("'(' expected after WRITE");
                Expression();
         /*       
         IncreaseOutProgram( PRINT, TOKENS[ TokenCounter-1 ].Number );
	*/
	 IncreaseOutProgram( PRINT, 0 );
	 token_type = TOKENS[ TokenCounter++ ].TokenType ;
	 if ( token_type != RIGHT_BRACKET ) 
	 	Error("')' expected");	
		return;
	   }         /* 'WRITE' operator */
	else if( token_type == IDENTIFIER )
	   {
#ifdef DEBUG1
	fprintf(stderr,"IDENTIFIER ");
#endif
		address = TOKENS[ TokenCounter-1 ].Number;
		token_type = TOKENS[ TokenCounter++ ].TokenType;
		if( token_type != ASSIGN )
			Error( "Assignment requires ':=' after identifier" );
#ifdef DEBUG1
	fprintf(stderr,"ASSIGNMENT \nStatement() calls Expression()\n");
#endif
                Expression();
                IncreaseOutProgram( STORE, address );
		return;
	   }        /* else if 'IDENTIFIER' */
	else if( token_type == WHILE )
	   {
                A1 = ProgramCounter;       /* Where control has to be 
                                              passed */ 
#ifdef DEBUG1
	fprintf(stderr,"Statement() calls Conditional()");
#endif 
                Conditional();
		A2 = ProgramCounter++;     /* The hole to place 
                                              JUMP_NO command */
		token_type = TOKENS[ TokenCounter++ ].TokenType;
		if( token_type != DO )
			Error( "WHILE cycle demands 'DO' after condition" );
#ifdef DEBUG1
         fprintf(stderr,"Statement() calls StatementList()\n");
#endif
                StatementList();
		token_type = TOKENS[ TokenCounter++ ].TokenType;
		if( token_type != OD )
			Error( "WHILE cycle has to be ended by 'OD' " );

                IncreaseOutProgram( JUMP, A1 ) ;

		OUTPUT_PROGRAM[ A2 ].Operation = JUMP_NO;
		OUTPUT_PROGRAM[ A2 ].Address   = ProgramCounter;
		return;
	   }        /* 'WHILE' */
	else if( token_type == IF )
	   {
                Conditional();
		A1 = ProgramCounter++;     /* The hole to place 
                                              JUMP_NO command */
		token_type = TOKENS[ TokenCounter++ ].TokenType;
		if( token_type != THEN )
			Error( "Conditional demands 'THEN' after condition" );
                StatementList();

		token_type = TOKENS[ TokenCounter++ ].TokenType;
		if( token_type == ELSE )
		   {         
			A2 = ProgramCounter++;     /* The hole to place JUMP 
                                                      command */
			OUTPUT_PROGRAM[ A1 ].Operation = JUMP_NO;
			OUTPUT_PROGRAM[ A1 ].Address   = ProgramCounter;
                        StatementList();
			OUTPUT_PROGRAM[ A2 ].Operation = JUMP;
			OUTPUT_PROGRAM[ A2 ].Address   = ProgramCounter;

                        token_type = TOKENS[ TokenCounter++ ].TokenType;
                         if( token_type != FI ) 
				Error( "Conditional demands 'FI' at the end" );
			        return; 
                 }            /* ELSE-FI part */
		else if( token_type != FI )
                        Error( "Conditional demands 'FI' at the end" );
			/* IF-FI (without ELSE) part */
                else
		   {
			OUTPUT_PROGRAM[ A1 ].Operation = JUMP_NO;
			OUTPUT_PROGRAM[ A1 ].Address   = ProgramCounter;
			return ;
		   } 
            /* IF-FI (without ELSE) part */
              }  /* IF part */
        else  Error( "Error in statement" );
   }

void Conditional()
   {
	TTokenType token_type;
	unsigned   number;
        Expression();
	token_type = TOKENS[ TokenCounter++ ].TokenType;
        if( token_type != RELATION )
		Error( "Conditional requires RELATION after expression" );
	else
	   number = TOKENS[ TokenCounter-1 ].Number;
        Expression();
        IncreaseOutProgram( COMPARE, number );
	return;
   }

void Expression()
   {
      TTokenType token_type;
      unsigned number;

      Term();
      while( TRUE )
         {
            token_type = TOKENS[ TokenCounter ].TokenType;
            number = TOKENS[ TokenCounter ].Number;
            if( token_type != ADD_SUB ) break;
            TokenCounter++;
            Term();
            if( number == 0 ) IncreaseOutProgram( ADD, 0 );
            else IncreaseOutProgram( SUB, 0 );
         }
      return;
   }

void Term()
   {
      TTokenType token_type;
      unsigned number;

      Primary();
      while( TRUE )
         {
            token_type = TOKENS[ TokenCounter ].TokenType;
            number = TOKENS[ TokenCounter ].Number;
            if( token_type != MULT_DIV ) break;
            TokenCounter++;
            Primary();
            if( number == 0 ) IncreaseOutProgram( MULT, 0 );
            else IncreaseOutProgram( DIV, 0 );
         }
      return;
   }

void Primary()
   {
	TTokenType token_type;
        unsigned number;

        token_type = TOKENS[ TokenCounter++ ].TokenType;

        if( token_type == IDENTIFIER )
	   {
             IncreaseOutProgram( LOAD, TOKENS[ TokenCounter-1 ].Number );
             return;
	   }
        else if( token_type == CONST )
	   {
             IncreaseOutProgram( LOAD,
                       TOKENS[ TokenCounter-1 ].Number + NumberOfVariables );
             return;
           }
        else if( token_type == READ )
	   {
             IncreaseOutProgram( INPUT, 0 );
             return;
	   }
        else if( token_type == LEFT_BRACKET )
	   {
             Expression();

             token_type = TOKENS[ TokenCounter++ ].TokenType;
             if( token_type != RIGHT_BRACKET )
                  Error( "Right bracket is absent" );
             else
                return;
	   }
        else if ( token_type == ADD_SUB )
           {
               number = TOKENS[ TokenCounter-1 ].Number;
               token_type = TOKENS[ TokenCounter++ ].TokenType;
               if( token_type != CONST ) Error( "Extra operation" );
               IncreaseOutProgram( LOAD,
                       TOKENS[ TokenCounter-1 ].Number + NumberOfVariables );
               if ( number == 1 ) IncreaseOutProgram( INVERT, 0 );
               return;
           }
        else Error( "Error in expression" );
   }

/*---------------------  Stack Machine Interpretor ---------------*/



/*-----------------------  Utilites ------------------------------*/

char *SMXName, *TPLName;
int main( int argc, char* argv[] )
  {
    
    if ( argc < 2 )
      {
         Error( "Usage: COMPILER.EXE <source text> [<SMX> <TPL>]" );
      }
    SourceFileName = argv[1];
    if( argc >= 3 )
    SMXName = argv[2];
    if( argc >= 4 )
    TPLName = argv[3];
    if( argc >= 5 ) Error("Too much arguments");
    
#ifdef DEBUG
	fprintf(stderr,"LexicalAnalyzer():CALLED\n");
#endif
    LexicalAnalyzer();
#ifdef DEBUG
	fprintf(stderr,"Program():CALLED\n");
#endif
    PrintTokenProgram();
/*    SyntaxAnalyzer(); */
    TokenCounter = 0;
    Program();
    PrintStackMachineProgram();
    return 0;
  }

void PrintTokenProgram ()
  {
    FILE *fp;
    int i,j;
    fp = fopen( TPLName,"wt" );
    if ( fp == NULL ) 
         {
         Alarm( "Can't open TPL file\n\t"
                "Listing is being written to stdout");
         fp = stdout ;
         } 
    for ( i=0; i < TokenCounter; i++ )
      {
        fprintf( fp, "%3d :  ", i );
        for ( j=0; j < TokenTypesNumber; j++ )
            if ( TOKENS[ i ].TokenType == TOKEN_TYPES[j].Type )
            {
             /* printf( TOKEN_TYPES[ j ] -> Name ); */
		fprintf( fp, "%-15s",TOKEN_TYPES[ j ].Name);
              break;
            }
        fprintf( fp, " %3d \n", TOKENS[ i ].Number );
      }
      if( fp != stdout )
      if( fclose( fp ) ) Alarm("Can't close TPL file");
  }

void PrintStackMachineProgram()
  {
    FILE *fp;
    int i,j;
    fp = fopen( SMXName,"wt" );
    if ( fp == NULL ) 
    	{
    		Alarm( "Can't open SMX module\n\t"
    		       "Stack Machine Program is written to stdout" );
    		fp = stdout ;
    	} 
    for ( i=0; i < ProgramCounter; i++ )
      {
        fprintf( fp, "%3d :  ", i );
        for ( j=0; j < SMOperationsNumber; j++ )
          if ( OUTPUT_PROGRAM[ i ].Operation == SM_OPERATIONS[ j ].Operation )
            {
              fprintf( fp, "%-15s",SM_OPERATIONS[ j ].Name );
              break;
            }
        fprintf( fp, " %3d \n", OUTPUT_PROGRAM[ i ]. Address );
      
  }
    if( fp != stdout ) 
    if ( fclose( fp )) Alarm("Can't close SMX module");
}
/*---------------------  End Compiler ----------------------------*/

