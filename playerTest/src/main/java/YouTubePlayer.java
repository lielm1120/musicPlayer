import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class YouTubePlayer {
    private WebDriver driver;
    private WebDriverWait wait;
    private static final long TIMEOUT_IN_SECONDS = 30;


    public YouTubePlayer() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless"); // Run in headless mode
        options.addArguments("--disable-gpu"); // Disable GPU usage
        options.addArguments("--no-sandbox"); // Bypass OS security model restrictions
        options.addArguments("--mute-audio"); // Mute audio to avoid sound interference
        options.addArguments("--disable-dev-shm-usage"); // Overcome resource limitations
        options.addArguments("window-size=1920x1080");
        driver = new ChromeDriver();
        wait = new WebDriverWait(driver, Duration.ofSeconds(TIMEOUT_IN_SECONDS));
    }

    public void playSong(String songName) {
        try {
            driver.get("https://www.youtube.com");
            WebElement searchBox = driver.findElement(By.name("search_query"));
            searchBox.sendKeys(songName);
            searchBox.submit();
            WebElement firstResult = wait.until((ExpectedConditions.
                    elementToBeClickable(By.xpath("//*[@lockup='true']"))));
            firstResult.click();
            skipAdIfPossible();
            waitForVideoToEnd();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    private void skipAdIfPossible() {
        try {
            WebElement skipButton = wait.until(ExpectedConditions
                    .elementToBeClickable(By.id("skip-button:3")));
            if (skipButton != null) {
                skipButton.click();
                System.out.println("Ad skipped.");
            }
        } catch (Exception e) {
            System.out.println("No skippable ad found or issue with locating the skip ad button.");
        }
    }

    private void waitForVideoToEnd() throws InterruptedException {
        JavascriptExecutor js = (JavascriptExecutor) driver;
        boolean isPlaying = true;

        while (isPlaying) {
            try {
                Double currentTime = (Double) js.executeScript("return document.querySelector('video').currentTime;");
                Double duration = (Double) js.executeScript("return document.querySelector('video').duration;");
                System.out.printf("%f ?= %f\n", currentTime, duration);
                if (currentTime >= (duration - 5)) {
                    isPlaying = false;
                } else {
                    Thread.sleep(1000);
                }
            } catch (Exception e) {
                System.out.println("Error while checking video end status. Retrying...");
            }
        }
    }

    public void close() {
        if (driver != null) {
            driver.quit();
        }
    }
}
