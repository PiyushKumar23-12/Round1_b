---

## 💻 How to Use

1. Clone the repository:
 
2. git clone https://github.com/PiyushKumar23-12/Round1_b
   
3. Put your PDFs into the collection/pdfs/ folder.
   
4. Place your input.json in collection folder. 

6. Run Docker Desktop/Engine.

7. Build and run the Docker container using the below commands in PowerShell:

   bash
   ```
   docker build -t round1b .;
   docker run --rm -it -v "${PWD}\collection:/app/collection" round1b
   ```

