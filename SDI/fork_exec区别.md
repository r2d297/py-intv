让我详细解释这两个重要的系统调用：

## **Fork() 系统调用**

### **基本概念**
`fork()` 创建一个与当前进程几乎完全相同的新进程（子进程）。

### **工作原理**
```c
#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>

int main() {
    pid_t pid;
    
    printf("Before fork: PID = %d\n", getpid());
    
    pid = fork();  // 这里进程"分叉"
    
    if (pid == 0) {
        // 子进程执行的代码
        printf("I'm child process, PID = %d, Parent PID = %d\n", 
               getpid(), getppid());
    } else if (pid > 0) {
        // 父进程执行的代码
        printf("I'm parent process, PID = %d, Child PID = %d\n", 
               getpid(), pid);
    } else {
        // fork失败
        perror("fork failed");
        return 1;
    }
    
    printf("Both processes execute this line\n");
    return 0;
}
```

### **执行结果**
```
Before fork: PID = 1234
I'm parent process, PID = 1234, Child PID = 1235
Both processes execute this line
I'm child process, PID = 1235, Parent PID = 1234
Both processes execute this line
```

### **Fork的返回值机制**
```c
void explain_fork_return() {
    pid_t result = fork();
    
    /*
     * fork()有三种可能的返回值：
     * 1. 在父进程中: 返回子进程的PID (> 0)
     * 2. 在子进程中: 返回 0
     * 3. 失败时: 返回 -1
     */
    
    switch (result) {
        case -1:
            perror("Fork failed");
            exit(1);
            
        case 0:
            printf("Child: My PID is %d\n", getpid());
            // 子进程特有的逻辑
            break;
            
        default:
            printf("Parent: Created child with PID %d\n", result);
            // 父进程特有的逻辑
            break;
    }
}
```

### **Fork的内存模型 (Copy-on-Write)**
```c
#include <sys/wait.h>

void demonstrate_cow() {
    int shared_var = 100;
    pid_t pid;
    
    pid = fork();
    
    if (pid == 0) {
        // 子进程修改变量
        shared_var = 200;
        printf("Child: shared_var = %d (address: %p)\n", 
               shared_var, &shared_var);
    } else {
        sleep(1);  // 确保子进程先执行
        printf("Parent: shared_var = %d (address: %p)\n", 
               shared_var, &shared_var);
        wait(NULL);  // 等待子进程结束
    }
}

/*
输出：
Child: shared_var = 200 (address: 0x7fff123456)
Parent: shared_var = 100 (address: 0x7fff123456)

注意：地址相同(虚拟地址)，但值不同(COW机制)
*/
```

## **Exec() 系列系统调用**

### **基本概念**
`exec()` 用当前进程加载并执行一个新程序，**替换**当前进程的内存映像。

### **Exec系列函数**
```c
#include <unistd.h>

// 主要的exec函数
int execl(const char *path, const char *arg, ...);
int execlp(const char *file, const char *arg, ...);
int execle(const char *path, const char *arg, ..., char *const envp[]);
int execv(const char *path, char *const argv[]);
int execvp(const char *file, char *const argv[]);
int execvpe(const char *file, char *const argv[], char *const envp[]);

/*
命名规律：
- l: 参数以列表形式传递 (list)
- v: 参数以数组形式传递 (vector)
- p: 在PATH环境变量中搜索程序 (path)
- e: 可以指定环境变量 (environment)
*/
```

### **Exec使用示例**
```c
// execl 示例
void example_execl() {
    printf("Before exec: PID = %d\n", getpid());
    
    // 执行 /bin/ls -l /home
    execl("/bin/ls", "ls", "-l", "/home", NULL);
    
    // 如果exec成功，这行代码永远不会执行
    printf("This line will never be printed\n");
}

// execv 示例
void example_execv() {
    char *args[] = {"ls", "-l", "/home", NULL};
    
    printf("Before exec: PID = %d\n", getpid());
    execv("/bin/ls", args);
    
    // 如果到达这里，说明exec失败了
    perror("execv failed");
}

// execlp 示例（在PATH中搜索）
void example_execlp() {
    printf("Before exec: PID = %d\n", getpid());
    
    // 不需要完整路径，会在PATH中搜索
    execlp("python3", "python3", "-c", "print('Hello from Python')", NULL);
    
    perror("execlp failed");
}
```

## **Fork + Exec 组合使用**

### **典型模式：创建新进程执行程序**
```c
#include <sys/wait.h>

void fork_exec_example() {
    pid_t pid;
    int status;
    
    pid = fork();
    
    if (pid == 0) {
        // 子进程：执行新程序
        printf("Child: About to exec 'ls'\n");
        
        execl("/bin/ls", "ls", "-l", ".", NULL);
        
        // 如果exec失败，才会执行到这里
        perror("exec failed");
        exit(1);
        
    } else if (pid > 0) {
        // 父进程：等待子进程完成
        printf("Parent: Waiting for child (PID: %d)\n", pid);
        
        wait(&status);  // 等待子进程结束
        
        if (WIFEXITED(status)) {
            printf("Child exited with status: %d\n", WEXITSTATUS(status));
        }
        
    } else {
        perror("fork failed");
    }
}
```

### **Shell实现的简化版本**
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

void simple_shell() {
    char command[256];
    char *args[64];
    char *token;
    int i;
    pid_t pid;
    
    while (1) {
        printf("simple_shell> ");
        fflush(stdout);
        
        // 读取用户输入
        if (!fgets(command, sizeof(command), stdin)) {
            break;
        }
        
        // 移除换行符
        command[strcspn(command, "\n")] = 0;
        
        // 退出命令
        if (strcmp(command, "exit") == 0) {
            break;
        }
        
        // 解析命令参数
        i = 0;
        token = strtok(command, " ");
        while (token != NULL && i < 63) {
            args[i++] = token;
            token = strtok(NULL, " ");
        }
        args[i] = NULL;
        
        if (args[0] == NULL) continue;  // 空命令
        
        // Fork + Exec 执行命令
        pid = fork();
        
        if (pid == 0) {
            // 子进程：执行命令
            execvp(args[0], args);
            perror("Command execution failed");
            exit(1);
            
        } else if (pid > 0) {
            // 父进程：等待命令完成
            wait(NULL);
            
        } else {
            perror("fork failed");
        }
    }
}
```

## **高级用法和技巧**

### **1. 重定向标准输入输出**
```c
void redirect_output() {
    int fd;
    pid_t pid;
    
    pid = fork();
    
    if (pid == 0) {
        // 子进程：重定向输出到文件
        fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
        
        if (fd == -1) {
            perror("open");
            exit(1);
        }
        
        // 重定向stdout到文件
        dup2(fd, STDOUT_FILENO);
        close(fd);
        
        // 执行命令，输出会写入文件
        execlp("ls", "ls", "-l", NULL);
        perror("exec");
        exit(1);
        
    } else {
        wait(NULL);
        printf("Command output saved to output.txt\n");
    }
}
```

### **2. 管道实现**
```c
void create_pipe_example() {
    int pipefd[2];
    pid_t pid1, pid2;
    
    // 创建管道
    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(1);
    }
    
    // 第一个子进程：执行 "ls -l"
    pid1 = fork();
    if (pid1 == 0) {
        close(pipefd[0]);  // 关闭读端
        dup2(pipefd[1], STDOUT_FILENO);  // 重定向stdout到管道写端
        close(pipefd[1]);
        
        execlp("ls", "ls", "-l", NULL);
        perror("exec ls");
        exit(1);
    }
    
    // 第二个子进程：执行 "grep txt"
    pid2 = fork();
    if (pid2 == 0) {
        close(pipefd[1]);  // 关闭写端
        dup2(pipefd[0], STDIN_FILENO);  // 重定向stdin到管道读端
        close(pipefd[0]);
        
        execlp("grep", "grep", "txt", NULL);
        perror("exec grep");
        exit(1);
    }
    
    // 父进程：关闭管道，等待子进程
    close(pipefd[0]);
    close(pipefd[1]);
    
    wait(NULL);  // 等待第一个子进程
    wait(NULL);  // 等待第二个子进程
}
```

### **3. 守护进程创建**
```c
void create_daemon() {
    pid_t pid;
    
    // 第一次fork
    pid = fork();
    if (pid < 0) {
        exit(1);
    }
    if (pid > 0) {
        exit(0);  // 父进程退出
    }
    
    // 子进程继续
    if (setsid() < 0) {  // 创建新会话
        exit(1);
    }
    
    // 第二次fork
    pid = fork();
    if (pid < 0) {
        exit(1);
    }
    if (pid > 0) {
        exit(0);  // 第一个子进程退出
    }
    
    // 现在是守护进程
    umask(0);  // 重置文件权限掩码
    chdir("/");  // 改变工作目录到根目录
    
    // 关闭标准文件描述符
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);
    
    // 守护进程的主逻辑
    while (1) {
        // 执行后台任务
        sleep(60);
    }
}
```

## **错误处理和最佳实践**

### **错误处理**
```c
void robust_fork_exec() {
    pid_t pid;
    int status;
    
    pid = fork();
    
    switch (pid) {
        case -1:
            // Fork失败
            perror("fork");
            exit(EXIT_FAILURE);
            
        case 0:
            // 子进程
            execl("/bin/nonexistent", "nonexistent", NULL);
            
            // Exec失败，子进程必须退出
            perror("exec");
            _exit(EXIT_FAILURE);  // 使用_exit，不调用atexit函数
            
        default:
            // 父进程
            if (waitpid(pid, &status, 0) == -1) {
                perror("waitpid");
                exit(EXIT_FAILURE);
            }
            
            if (WIFEXITED(status)) {
                printf("Child exited normally with status %d\n", 
                       WEXITSTATUS(status));
            } else if (WIFSIGNALED(status)) {
                printf("Child terminated by signal %d\n", 
                       WTERMSIG(status));
            }
            break;
    }
}
```

## **性能和内存考虑**

### **Fork的开销**
```c
// Fork对大进程的影响
void large_process_fork() {
    // 分配大量内存
    char *large_memory = malloc(100 * 1024 * 1024);  // 100MB
    memset(large_memory, 'A', 100 * 1024 * 1024);
    
    printf("Before fork: allocated 100MB\n");
    
    pid_t pid = fork();
    
    if (pid == 0) {
        // 子进程：由于COW机制，不会立即复制这100MB
        printf("Child: forked successfully\n");
        
        // 只有修改内存时才会触发实际复制
        large_memory[0] = 'B';  // 这会触发页面复制
        
        exit(0);
    } else {
        wait(NULL);
        free(large_memory);
    }
}
```

## **总结对比**

### **Fork vs Exec**
| 特性 | Fork | Exec |
|------|------|------|
| **目的** | 创建新进程 | 替换当前程序 |
| **内存** | 复制父进程内存 | 替换当前内存映像 |
| **PID** | 子进程获得新PID | 保持相同PID |
| **返回值** | 父进程返回子PID，子进程返回0 | 成功不返回，失败返回-1 |
| **使用场景** | 多进程编程 | 程序启动/替换 |

### **常见组合模式**
```c
// 1. Fork + Exec + Wait：执行外部程序
pid = fork();
if (pid == 0) {
    exec(...);
} else {
    wait(NULL);
}

// 2. Fork + 不同逻辑：并行处理
pid = fork();
if (pid == 0) {
    do_child_work();
} else {
    do_parent_work();
}

// 3. Fork + Exec + 管道：进程间通信
pipe(fd);
pid = fork();
if (pid == 0) {
    setup_pipe();
    exec(...);
} else {
    setup_pipe();
    communicate_with_child();
}
```

Fork和Exec是Unix/Linux系统进程管理的基础，理解它们的工作原理对于系统编程和操作系统理解都非常重要。它们的组合使用模式是现代操作系统实现多进程、shell、服务器等应用的核心机制。