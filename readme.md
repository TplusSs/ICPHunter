# ICPHunter

## 一、项目概述

ICPHunter 是一个使用 Python 编写的命令行工具，其核心功能是查询网站域名的 ICP 备案信息。它支持多种输入方式，既可以针对单个域名、URL 或者企业名进行查询，也能通过文件批量处理多个查询项。查询结果将以 Excel 文件的形式保存，文件名采用输入的公司名称或域名，方便用户查看和管理。

## 二、功能特性

1. **多样化输入方式**：支持单个域名、URL 或企业名的查询，同时也支持从文件中批量读取查询项。
2. **Excel 结果输出**：将查询到的备案信息保存为 Excel 文件，便于后续分析和处理。
3. **多线程并发处理**：利用线程池技术，预设并发数量为 50，提高查询效率，可根据实际情况调整并发数。

## 三、安装指南

### 依赖安装

在运行本项目之前，需要安装所需的依赖库。可以使用以下命令进行安装：

```bash
pip install requests beautifulsoup4 click pandas openpyxl
```

## 四、使用方法

### 单个查询

若要查询单个域名、URL 或者企业名的 ICP 备案信息，可使用 `-d` 或 `--domain` 选项，示例如下：

```bash
python main.py -d baidu.com
```

执行上述命令后，查询结果将保存为 `baidu.com.xlsx` 文件。

也可以直接查询公司名称，示例如下：

```bash
python main.py -d 深圳市腾讯计算机系统有限公司
```

执行上述命令后，查询结果将保存为深圳市腾讯计算机系统有限公司文件。

### 批量查询

若有多个查询项，可将它们逐行写入一个文本文件中，然后使用 `-f` 或 `--file` 选项指定该文件，示例如下：

```bash
python main.py -f domains.txt
```

程序会为每个查询项生成对应的 Excel 文件，文件名即为查询项。

## 五、代码结构

### 主要文件

- `main.py`：项目的主程序文件，包含命令行接口和核心业务逻辑。
- `requirements.txt`：记录项目所需的依赖库列表，方便快速安装。

### 主要函数

- `get_uuid()`：生成唯一的 UUID 用于请求的 Cookie。
- `get_root_domain(input_url)`：从输入的 URL 中提取根域名。
- `contains_chinese(s)`：判断字符串中是否包含中文字符。
- `build_url_xpath(input)`：根据输入构建查询的 URL。
- `fetch_data(url)`：发送 HTTP 请求获取网页内容。
- `handle_data_xpath(data, output_filename)`：解析网页内容，提取备案信息并保存为 Excel 文件。
- `fetch_and_handle_data_xpath(url, output_filename)`：调用 `fetch_data` 和 `handle_data_xpath` 完成单个查询的处理。
- `process_file(filename)`：处理文件中的多个查询项，使用线程池并发执行。
- `main(domain, file)`：命令行接口的主函数，根据用户输入调用相应的处理函数。

## 六、注意事项

1. **网络连接**：确保你的网络连接正常，因为程序需要访问 `https://www.beianx.cn` 网站进行查询。
2. **并发数量**：由于使用了多线程处理，预设的并发数量为 50。请根据实际情况和目标服务器的承受能力来调节该值，过大的并发请求可能会对目标服务器产生压力。

## 七、贡献与反馈

如果你在使用过程中遇到问题，或者有任何改进建议，欢迎在 GitHub 仓库中提交 issue 或 pull request。

## 八、许可证

本项目采用 [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) 许可证。

## 九、联系方式

如果你有任何疑问或建议，可以通过以下方式联系我：

- **邮箱**：tyc9114@gmail.com
- **微信**：TplusSs

