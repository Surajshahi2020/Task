import csv, datetime
from rest_framework import serializers

from task.models import Location
from common.exceptions import UnprocessableEntityException


class TaskSerializer(serializers.Serializer):
    file = serializers.FileField(write_only=True)

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        file = data.get("file")
        if not file.name.endswith(".csv"):
            raise UnprocessableEntityException(
                {
                    "title": "File Read",
                    "message": "Invalid file format. Only CSV files are allowed.",
                }
            )
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        file = validated_data.get("file")
        file_data = file.read().decode("utf-8")
        csv_data = csv.DictReader(file_data.splitlines())
        filtered_data = []
        for row in csv_data:
            if all(row.get(key) != "" for key in row):
                filtered_data.append(row)

        for row in filtered_data:
            agreement_date_str = row["Agreement Date"]
            agreement_date = (
                datetime.datetime.strptime(agreement_date_str, "%m/%d/%Y")
                .date()
                .strftime("%Y-%m-%d")
            )

            government = Location(
                province=row["Province"],
                district=row["District"],
                muncipality=row["Municipality"],
                project_title=row["Project Title"],
                project_status=row["Project Status"],
                donor=row["Donor"],
                executing_agency=row["Executing Agency"],
                implementing_partner=row["Implementing Partner"],
                counterpart_ministry=row["Counterpart Ministry"],
                type_of_assistance=row["Type of Assistance"],
                budget_type=row["Budget Type"],
                humanitarian=row["Humanitarian"],
                sector=row["Sector"],
                agreement_date=agreement_date,
                commitments=row["Commitments"],
                disbursement=row["Disbursement"],
            )
            government.save()
        return Location()


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
