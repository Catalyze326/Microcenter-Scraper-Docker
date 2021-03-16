import org.openqa.selenium.By
import org.openqa.selenium.WebDriver
import org.openqa.selenium.WebElement
import org.openqa.selenium.firefox.FirefoxDriver
import org.openqa.selenium.firefox.FirefoxOptions
import org.openqa.selenium.remote.RemoteWebDriver
import org.openqa.selenium.support.ui.ExpectedConditions
import org.openqa.selenium.support.ui.WebDriverWait
import java.lang.Thread.sleep
import java.net.URL
import java.sql.*

class Scrape {
    /**
     * @param store String value of the store name in the website
     */
    private fun scrape_store(store: String) {
//        val options = FirefoxOptions()
//        val url = URL("http://selenium-microcenter:4444")
//        val driver = RemoteWebDriver(url, options)
        val driver = FirefoxDriver()
        driver.get("https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=44+42+40+41+37+23+36+38+39+22+43+24+46+47+45&myStore=true")
        val ec = ExpectedConditions.visibilityOfElementLocated(By.id("storeInfo"))
        WebDriverWait(driver, 10).until(ec)
        val listOfSites = driver.findElements(By.className("dropdown-itemLI"))
        listOfSites.firstOrNull{it.text == store}?.click()
        val xpath = "//a[contains(@id, 'hypProduct')]"
        val items = driver.findElements(By.xpath(xpath))
        for (item in items) parse_item(item, store).forEach { print(this) }
    }

    private fun parse_item(item: WebElement, store: String): Array<String> {
        val name = item.getAttribute("data-name")
        val price = item.getAttribute("data-price")
        val brand = item.getAttribute("data-brand")
        val category = item.getAttribute("data-category")
        val url: String = item.getAttribute("href")
        return arrayOf(name, price, brand, category, url, store)
    }

    private fun send_to_db(values: Array<String>) {
        val con = DriverManager.getConnection(
            "jdbc:mysql://mariadb-microcenter-java/microcenter",
            "microcenter", "2Pn36D3iM8vnTAul")
        val mysql_stmt = "INSERT INTO microcenter VALUES(TRUE,?, NULL, NULL,?,?,?,?,?);"
        val stmt = con.prepareStatement(mysql_stmt)
        stmt.setDouble(2, values[1].toDouble())
        stmt.setString(1, values[0])
        stmt.setString(3, values[2])
        stmt.setString(4, values[3])
        stmt.setString(5, values[4])
        stmt.setString(6, values[5])
        stmt.executeUpdate()
        for (value in values) println(value)
    }

    constructor (store: String) {
//        val con = DriverManager.getConnection(
//            "jdbc:mysql://mariadb-microcenter/microcenter",
//            "microcenter", "2Pn36D3iM8vnTAul")
//        val mysql_drop_stmt = "DROP TABLE IF EXISTS microcenter;"
//        val stmt = con.prepareStatement(mysql_drop_stmt)
//        stmt.executeUpdate()
//        val mysql_create_stmt = "CREATE TABLE IF NOT EXISTS microcenter (" +
//                " is_new boolean," +
//                " name VARCHAR(256)," +
//                " price DOUBLE," +
//                " open_box_price DOUBLE," +
//                " percent_difference_price DOUBLE," +
//                " category VARCHAR(48)," +
//                " brand VARCHAR(128)," +
//                " url VARCHAR(256)," +
//                " store VARCHAR(32)" +
//                ");"
//        val stmt_create = con.prepareStatement(mysql_create_stmt)
//        stmt_create.executeUpdate()
        scrape_store(store)
    }
}

fun main() {
    sleep(12000)
    Scrape("MD - Parkville");
    Scrape("MD - Rockville");
    Scrape("VA - Fairfax");
}