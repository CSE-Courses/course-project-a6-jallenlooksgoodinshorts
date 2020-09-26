import java.sql.*;

public class register{

    public static void testConn(){
        try {
            Class.forName("com.mysql.jdbc.Driver");
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/userdata","kgood","cse442a6");
            System.out.println("Connected");
            conn.close();
        } catch (SQLException | ClassNotFoundException e) {
            System.out.println("No Connection");
        }

    }

    public static void newUser(String email,String password,String fname,String lname,String username){
        String inputValues = "INSERT INTO users VALUES(?,?,?,?,?);";
        try {
            Class.forName("com.mysql.jdbc.Driver"); //Creates jdbc Driver
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/userdata","kgood","cse442a6"); //Connects to mysql server ***will need to change url***
            System.out.println("Connected");
            PreparedStatement st = conn.prepareStatement(inputValues); //creates sql string from arguments
            st.setString(1,email);
            st.setString(2,password);
            st.setString(3,fname);
            st.setString(4,lname);
            st.setString(5,username);
            int rowAffected = st.executeUpdate(); //Calls sql query on database specified in connection url
            if(rowAffected>0){
                System.out.println("Table updated Successfully.");
            }
            conn.close();
            System.out.println("Connection Closed.");
        } catch (SQLException | ClassNotFoundException e) {
            e.getMessage();
            e.printStackTrace();

        }

    }
}