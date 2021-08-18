import os
import oss2

from typing import Optional


class OSS():
    """
    对云存储进行操作

    用法 ::

        >>> import oss
        >>> bucket = oss.OSS(
                access_key_id='<your access_key_id>',
                access_key_secret='<your access_key_secret>',
                bucket_name='<your bucket_name>',
                endpoint='<your endpoint>',
            )
    """
    def __init__(self,
        access_key_id: str,
        access_key_secret: str,
        bucket_name: str,
        endpoint: str
    ):
        # 确认上面的参数都填写正确了
        for param in (access_key_id, access_key_secret, bucket_name, endpoint):
            assert '<' not in param, '请设置参数：' + param

        # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
        self.bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)


    def upload_img(self, dirname: Optional[str], filename: str) -> None:
        """
        上传图片
        :param dirname: 图片上传到云存储的文件夹名
        :param filename: 图片的文件名

        用法 ::

            >>> bucket.upload_img(dirname='bottles_dev/', filename='1.jpg')

        """
        key = dirname + filename
        self.bucket.put_object_from_file(key=key, filename=filename)


    def download_img(self, dirname: Optional[str], filename: str) -> None:
        """
        下载到本地文件
        :param dirname: 图片在云存储的文件夹名
        :param filename: 图片的文件名

        用法 ::

            >>> bucket.download_img(dirname='bottles_dev/', filename='1.jpg')

        """
        key = dirname + filename
        self.bucket.get_object_to_file(key, filename)


    def delete_files(self, dirname: str) -> None:
        """
        批量删除文件下的所有文件
        :param dirname: 云存储的文件夹名

        用法 ::

            >>> bucket.delete_files(dirname='bottles_dev/')

        """
        prefix = dirname
        # 删除指定前缀的文件。
        for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
            self.bucket.delete_object(obj.key)


if __name__ == '__main__':
    bucket = OSS(
        access_key_id=os.getenv('ACCESS_KEY_ID'),
        access_key_secret=os.getenv('ACCESS_KEY_SECRET'),
        bucket_name=os.getenv('OSS_BUCKET_NAME'),
        endpoint=os.getenv('OSS_ENDPOINT'),
    )
    # bucket.upload_img(dirname='bottles_dev/', filename='1.jpg')
    # bucket.download_img(dirname='bottles_dev/', filename='1.jpg')
    bucket.delete_files(dirname='bottles_dev/')
