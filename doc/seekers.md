# Seekers

## 关于Seeker

Seeker 是指检查番剧更新的检查器，通常通过传入检查信息，执行检查函数来调用，并返回检查结果。

Seeker 通常检查的是番剧当前观看集数的下一集资源。

在本项目中，所有的 seeker 都保存在 `anicolle/seeker` 文件夹下，并作为 seeker 包的子模块来使用。

## Seeker 的标准结构

可以参考源代码中的 `popgo.py` 和 `bilibili.py` 两个 seeker 来撰写 seeker，这里指出一些在编写时特别需要注意的事项。

每一个 seeker module 必须包含一个函数，其原型如下：

    seek( chk_key, cur_epi )
        Returns seek result dictionary.

其参数 chk_key 为番剧数据中的检查关键字，cur_epi 为番剧数据中的当前看到的集数(current episode)。

该函数的返回值是一个 dict，其结构如下。

    {
        title: '' #下一集资源的标题
        link: '' #下一集资源的连接
    }

该返回数据将被 anicolle.core 模块检索到，并加入番组的 check up 结果中。

另需注意，chk_key 需要满足一定的鲁棒性，例如在示例的 bilibili seeker 中，其能够判断参数 chk_key 给出的是检索关键词还是番剧 Series ID，从而进行不同的逻辑操作。
这种性质大大简化了番剧数据中 chk_key 的编写。

## 注册 Seeker

Seeker 被编写完成后，需要加入 seeker package 的构造文件中。在 `seeker/__init__.py` 中需要
首先 import 需要注册的 Seeker 之模块，再将其名称写入该构造文件中名为 seeker 的 dict 中。

seeker dict 的key 为所注册的 seeker 之名称，value 为所导入的模块。
