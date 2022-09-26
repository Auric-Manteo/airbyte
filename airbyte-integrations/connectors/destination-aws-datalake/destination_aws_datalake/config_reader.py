#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

import enum


class CredentialsType(enum.Enum):
    IAM_ROLE = "IAM Role"
    IAM_USER = "IAM User"

    @staticmethod
    def from_string(s: str):
        if s == "IAM Role":
            return CredentialsType.IAM_ROLE
        elif s == "IAM User":
            return CredentialsType.IAM_USER
        else:
            raise ValueError(f"Unknown auth mode: {s}")


class OutputFormat(enum.Enum):
    PARQUET = "Parquet"
    JSONL = "JSONL"

    @staticmethod
    def from_string(s: str):
        if s == "Parquet":
            return OutputFormat.PARQUET
        elif s == "JSONL":
            return OutputFormat.JSONL
        else:
            raise ValueError(f"Unknown output format: {s}")


class CompressionCodec(enum.Enum):
    SNAPPY = "SNAPPY"
    GZIP = "GZIP"
    ZSTD = "ZSTD"
    UNCOMPRESSED = "UNCOMPRESSED"

    @staticmethod
    def from_config(str: str):
        if str == "SNAPPY":
            return CompressionCodec.SNAPPY
        elif str == "GZIP":
            return CompressionCodec.GZIP
        elif str == "ZSTD":
            return CompressionCodec.ZSTD
        elif str == "UNCOMPRESSED":
            return CompressionCodec.UNCOMPRESSED
        else:
            raise ValueError(f"Unknown compression codec: {str}")


class PartitionOptions(enum.Enum):
    NONE = "NO PARTITIONING"
    DATE = "DATE"
    YEAR = "YEAR"
    MONTH = "MONTH"
    DAY = "DAY"
    YEAR_MONTH = "YEAR/MONTH"
    YEAR_MONTH_DAY = "YEAR/MONTH/DAY"

    @staticmethod
    def from_string(s: str):
        if s == "NO PARTITIONING":
            return PartitionOptions.NONE
        elif s == "DATE":
            return PartitionOptions.DATE
        elif s == "YEAR":
            return PartitionOptions.YEAR
        elif s == "MONTH":
            return PartitionOptions.MONTH
        elif s == "DAY":
            return PartitionOptions.DAY
        elif s == "YEAR/MONTH":
            return PartitionOptions.YEAR_MONTH
        elif s == "YEAR/MONTH/DAY":
            return PartitionOptions.YEAR_MONTH_DAY
        else:
            raise ValueError(f"Unknown partition option: {s}")


class ConnectorConfig:
    def __init__(
        self,
        aws_account_id: str = None,
        region: str = None,
        credentials: dict = None,
        bucket_name: str = None,
        bucket_prefix: str = None,
        lakeformation_database_name: str = None,
        table_name: str = None,
        format: dict = None,
        partitioning: dict = None,
    ):
        self.aws_account_id = aws_account_id
        self.credentials = credentials
        self.credentials_type = CredentialsType.from_string(credentials.get("credentials_title"))
        self.region = region
        self.bucket_name = bucket_name
        self.bucket_prefix = bucket_prefix
        self.lakeformation_database_name = lakeformation_database_name
        self.table_name = table_name

        self.format_type = OutputFormat.from_string(format.get("format_type"))
        self.compression_codec = CompressionCodec.from_config(format.get("compression_codec"))

        self.partitioning = PartitionOptions.from_string(partitioning)

        if self.credentials_type == CredentialsType.IAM_USER:
            self.aws_access_key = self.credentials.get("aws_access_key_id")
            self.aws_secret_key = self.credentials.get("aws_secret_access_key")
        elif self.credentials_type == CredentialsType.IAM_ROLE:
            self.role_arn = self.credentials.get("role_arn")
        else:
            raise Exception("Auth Mode not recognized.")

    def __str__(self):
        return f"<S3Bucket(AwsAccountId={self.aws_account_id},Region={self.region},Bucket={self.bucket_name}>"
