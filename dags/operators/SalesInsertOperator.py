class InsertSalesOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            name: str,
            mysql_conn_id: str,
            database: str,
            *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.inserts = inserts
        self.postgres_conn_id = postgres_conn_id
        self.database = database

    def execute(self, context):
        src = PostgresHook(postgres_conn_id=self.postgres_conn_id,schema=self.database)
        src_conn = src.get_conn()
        cursor = src_conn.cursor()

        names = ['Paul', 'Andres', 'Aymaru','Julio','Stward']

        for i in range(0,self.inserts):
            rand_name = randrange(0,len(names))
            rand_amount = randrange(10000,500000)

            cursor.execute ("INSERT INTO sales(name,amount) VALUES ( %(name)s, %(amount)s )", {'name':names[rand_name],'amount':rand_amount})
        cursor.commit()
        cursor.close()
        return
